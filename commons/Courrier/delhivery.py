import requests
from django.conf import settings


class Delhivery:
    def __init__(self, *arg, **kwargs):
        self.api_token = settings.DELHIVERY_API_KEY

    # Request to delhivery
    def request_to_delhivery(self, url, payload, method="GET"):
        headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json"
        }
        try:
            if method == "GET":
                response = requests.get(url, params=payload, headers=headers)
                return response.status_code, response.json()
            elif method == "POST":
                response = requests.post(url, data=payload, headers=headers)
                return response.status_code, response.json()
        except:
            return 500, {"message": "Error", "status": "fail"}

    def check_pincode(self, pincode):
        url = 'https://track.delhivery.com/c/api/pin-codes/json/'
        payload = {
            'filter_codes': pincode
        }
        # false_return = (200, {
        #     "delivery_codes": [
        #         {
        #             "postal_code": {
        #                 "repl": "Y",
        #                 "pin": 855107,
        #                 "max_amount": 0,
        #                 "pre_paid": "Y",
        #                 "cash": "Y",
        #                 "max_weight": 0,
        #                 "pickup": "Y",
        #                 "district": "Kishanganj",
        #                 "covid_zone": "G",
        #                 "country_code": "IN",
        #                 "is_oda": "N",
        #                 "sort_code": "KNE/CNT",
        #                 "state_code": "BR",
        #                 "cod": "Y"
        #             }
        #         }
        #     ]
        # })
        # return false_return
        return self.request_to_delhivery(url, payload)

    def create_order(self, data, payment_mode='COD'):
        # payment_mode: options: Prepaid/COD/Pickup/REPL
        payload = {
            "pickup_location": {
                "name": "PUNAM EXPRESS"
            },
            "shipments": [{
                "add": data['street_address'],  # (mandatory)
                "address_type": "",  # (optional)
                "phone": data['mobile_number'],  # (mandatory)
                "payment_mode": payment_mode,  # (mandatory)
                "name": data['full_name'],  # (mandatory)
                "pin": data['postal_code'],  # (mandatory)
                "order": data['order_id'],  # (mandatory)

                "products_desc": data['product_description'],  # Description of product which is used in shipping label
                "cod_amount": data['cod_amount'],

                "weight": data['weight'],  # (optional)
                "shipment_height": data['shipment_height'],  # (optional)
                "shipment_width": data['shipment_width'],  # (optional)
                "shipment_length": data['shipment_length'],  # (optional)
                "category_of_goods": data['category_of_goods'],  # (optional)
            }]
        }
        url = 'https://track.delhivery.com/api/cmu/create.json'
        payload = 'format=json&data={}'.format(payload).replace("'", '"')

        # false_return = (200, {
        #     'cash_pickups_count': 0.0,
        #     'package_count': 1,
        #     'upload_wbn': 'UPL5842124732277212440',
        #     'replacement_count': 0,
        #     'pickups_count': 0,
        #     'packages': [{
        #         'status': 'Success',
        #         'client': 'PUNAM EXPRESS',
        #         'sort_code': 'SIG/FLR',
        #         'remarks': [''],
        #         'waybill': '4244610034635',
        #         'cod_amount': 201.96,
        #         'payment': 'COD',
        #         'serviceable': True,
        #         'refnum': '12'
        #     }],
        #     'cash_pickups': 0.0,
        #     'cod_count': 1,
        #     'success': True,
        #     'prepaid_count': 0,
        #     'cod_amount': 201.96
        # })
        # return false_return
        return self.request_to_delhivery(url, payload, 'POST')

    def track_order(self, tracking_number):
        url = 'https://track.delhivery.com/api/v1/packages/json/'
        payload = {
            "waybill": tracking_number
        }
        return self.request_to_delhivery(url, payload)
