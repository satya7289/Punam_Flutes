from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages

from commons.Courrier.delhivery import Delhivery
from commons.Courrier.ecom import ECOM
from order.models import Order, CourrierOrder


class CheckForCourrier(View):
    message = 'fail'
    status = '0'
    delhivery = Delhivery()
    ecom = ECOM()
    json_res = {
        'message': message,
        'status': status,
    }

    def get(self, request):
        order_id = request.GET.get('order_id')
        if order_id:
            order = Order.objects.filter(id=order_id).first()
            if order:
                pincode = order.shipping_address.postal_code

                # Check with Delhivery Courrier
                status_code, res = self.delhivery.check_pincode(pincode)
                if status_code == 200:
                    self.json_res['delhivery'] = '1' if len(res) > 0 else '0'
                    self.json_res['delhivery_data'] = res
                    self.json_res['status'] = '1'
                    self.json_res['message'] = "success"

                # Check With Ecom Courrier
                status_code, res = self.ecom.check_pincode(pincode)
                if status_code == 200:
                    self.json_res['ecom'] = '0' if res.get('message') else '1'
                    self.json_res['ecom_data'] = res
                    self.json_res['status'] = '1'
                    self.json_res['message'] = "success"

        return JsonResponse(self.json_res)


class CreateOrderForCourrier(View):
    delhivery = Delhivery()

    def post(self, request):
        print(request.POST)
        order_id = request.POST.get('order_id')
        courrier = request.POST.get('courrier')
        height = request.POST.get('height')
        width = request.POST.get('width')
        length = request.POST.get('length')
        message = "Opps, something went wrong try again with courrier services"

        order = Order.objects.filter(id=order_id).first()
        if order:
            shipping_address = order.shipping_address
            payment_mode = 'COD' if(order.payment.method == 'COD' and not order.status) else 'Prepaid'
            data = {
                'street_address': shipping_address.street_address,
                'mobile_number': shipping_address.mobile_number,
                'full_name': shipping_address.full_name,
                'postal_code': shipping_address.postal_code,
                'order_id': order.id,
                'product_description': '',
                'cod_amount': order.total if payment_mode == 'COD' else 0,
                'weight': '',
                'shipment_height': height,
                'shipment_width': width,
                'shipment_length': length,
                'category_of_goods': '',
            }
            if courrier == 'delhivery':
                status_code, resp = self.delhivery.create_order(data, payment_mode)
                try:
                    if status_code == 200:
                        tracking_number = resp['packages'][0]['waybill']
                        CourrierOrder.objects.update_or_create(
                            order=order,
                            defaults={'courrier': courrier, 'tracking_number': tracking_number}
                        )
                        message = f"Courrier Booked with {courrier}; Tracking number is {tracking_number}"
                except:
                    pass

        messages.add_message(request, messages.WARNING, message)
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class TrackCourrierOrder(View):
    delhivery = Delhivery()
    ecom = ECOM()

    def get(self, request):
        order_id = request.GET.get('order_id')
        json_resp = {
            "message": "fail"
        }
        order = Order.objects.filter(id=order_id).first()
        if order:
            courrierorder = order.courrierorder
            # courrierorder.courrier = 'ecom'
            # courrierorder.tracking_number = '860904688'
            if courrierorder and courrierorder.tracking_number:
                tracking_number = courrierorder.tracking_number
                if courrierorder.courrier == 'Delhivery' or courrierorder.courrier == 'delhivery':
                    status_code, resp = self.delhivery.track_order(tracking_number)
                    if status_code == 200:
                        json_resp = {
                        "message": "success",
                        "courrier": 'delhivery',
                        "tracking_number": tracking_number, 
                        "resp": resp
                    }
                elif courrierorder.courrier == 'ECOM' or courrierorder.courrier == 'ecom':
                    status_code, resp = self.ecom.track_order(tracking_number)
                    if status_code == 200:
                        json_resp = {
                            "message": "success",
                            "courrier": "ecom",
                            "tracking_number": tracking_number, 
                            "resp": resp
                        }
                    # print(resp)
        return JsonResponse(json_resp)
