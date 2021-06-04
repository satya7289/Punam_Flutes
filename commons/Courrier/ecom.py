import json
import requests
from django.conf import settings
from xml.etree import ElementTree


class ECOM:
    def __init__(self, *arg, **kwargs):
        self.username = settings.ECOM_USERNAME
        self.password = settings.ECOM_PASSWORD

    # Request to ecom
    def request_to_ecom(self, url, payload, method="GET", json_resp=True):
        payload['username'] = self.username
        payload['password'] = self.password
        try:
            if method == "GET":
                response = requests.get(url, params=payload)
                if json_resp:
                    return response.status_code, response.json()
                return response.status_code, response
            elif method == "POST":
                response = requests.post(url, data=payload)
                if json_resp:
                    return response.status_code, response.json()
                return response.status_code, response
        except:
            return 500, {"message": "Error", "status": "fail"}

    def check_pincode(self, pincode):
        url = 'https://api.ecomexpress.in/apiv2/pincodes/'
        status_code, resp = self.request_to_ecom(url, {}, "POST")
        if status_code == 200:
            for res in resp:
                if res.get('pincode') and pincode == str(res.get('pincode')):
                    return 200, res
            return 200, {"message": "Not found", "status": "fail"}
        return resp

    def track_order(self, tracking_number):
        url = 'https://plapi.ecomexpress.in/track_me/api/mawbd/'
        payload = {
            "awb": tracking_number
        }
        status_code, resp = self.request_to_ecom(url, payload, "GET", False)
        data = []
        if status_code == 200:
            resp_tree = ElementTree.fromstring(resp.content)
            scans = resp_tree.find('object/field/.[@name="scans"]')
            for scan in scans:
                res = {}
                res['date'] = scan.find('./field[@name="updated_on"]').text
                res['status'] = scan.find('./field[@name="status"]').text
                res['location_city'] = scan.find('./field[@name="location_city"]').text
                data.append(res)
            return status_code, data
        return status_code, data

    def create_waybill(self, payment_mode):
        # payment_method = PPD /COD /REV
        payment_mode = 'PPD' if payment_mode == 'Prepaid' else payment_mode
        url = 'https://api.ecomexpress.in/apiv2/fetch_awb/'
        payload = {
            'count': 1,
            'type': payment_mode
        }
        return self.request_to_ecom(url, payload, "POST")

    def create_order(self, data, payment_mode='COD'):
        # payment_mode: options: COD/PPD
        payment_mode = 'PPD' if payment_mode == 'Prepaid' else payment_mode
        json_input = {
            "AWB_NUMBER": data.get('tracking_number'),  # (mandatory)
            "ORDER_NUMBER": str(data.get('order_id')),  # (mandatory)
            "PRODUCT": payment_mode,
            "CONSIGNEE": data.get('full_name'),  # (mandatory)
            "CONSIGNEE_ADDRESS1": data.get('street_address'),  # (mandatory)
            "CONSIGNEE_ADDRESS2": "",
            "CONSIGNEE_ADDRESS3": "",
            "DESTINATION_CITY": data.get('city'),  # (mandatory)
            "PINCODE": data.get('postal_code'),  # (mandatory)
            "STATE": data.get('state'),  # (mandatory)
            "MOBILE": data.get('mobile_number'),  # (mandatory)
            "TELEPHONE": "0123456789",
            "ITEM_DESCRIPTION": data.get('product_description'),  # (mendatory)
            "PIECES": 1,
            "COLLECTABLE_VALUE": data.get('cod_amount'),
            "DECLARED_VALUE": 1,
            "ACTUAL_WEIGHT": float(data.get('weight')),  # (optional)
            "VOLUMETRIC_WEIGHT": 0,  # (optional)
            "LENGTH": float(data.get('shipment_length')),  # (optional)
            "BREADTH": float(data.get('shipment_width')),  # (optional)
            "HEIGHT": float(data.get('shipment_height')),  # (optional)
            "PICKUP_NAME": "PUNAM FLUTES",
            "PICKUP_ADDRESS_LINE1": "A 58, Jawahar Park, Deoli road, Khanpur New Delhi 110062 Phone :8505922922",
            "PICKUP_ADDRESS_LINE2": "",
            "PICKUP_PINCODE": "110062",
            "PICKUP_PHONE": "991118668",
            "PICKUP_MOBILE": "8505922922",
            "RETURN_NAME": "PUNAM FLUTES",
            "RETURN_ADDRESS_LINE1": "A 58, Jawahar Park, Deoli road, Khanpur New Delhi 110062 Phone :8505922922",
            "RETURN_ADDRESS_LINE2": "",
            "RETURN_PINCODE": "110062",
            "RETURN_PHONE": "991118668",
            "RETURN_MOBILE": "8505922922",
            "ADDONSERVICE": [""],
            "DG_SHIPMENT": "false",
            "ADDITIONAL_INFORMATION": {
                "essentialProduct": "N",
                "OTP_REQUIRED_FOR_DELIVERY": "N",
                "DELIVERY_TYPE": "",
                "SELLER_TIN": "",
                "INVOICE_NUMBER": "",
                "INVOICE_DATE": "",
                "ESUGAM_NUMBER": "",
                "ITEM_CATEGORY": "Musical Instrument or Case",
                "PACKING_TYPE": "WH",
                "PICKUP_TYPE": "WH",
                "RETURN_TYPE": "WH",
                "CONSIGNEE_ADDRESS_TYPE": "WH",
                "PICKUP_LOCATION_CODE": "",
                "SELLER_GSTIN": "07ANLPP2290D1ZY",
                "GST_HSN": "",
                "GST_ERN": "",
                "GST_TAX_NAME": "",
                "GST_TAX_BASE": "",
                "DISCOUNT": "",
                "GST_TAX_RATE_CGSTN": "0.0",
                "GST_TAX_RATE_SGSTN": "0.0",
                "GST_TAX_RATE_IGSTN": "0.0",
                "GST_TAX_TOTAL": "0.0",
                "GST_TAX_CGSTN": "0.0",
                "GST_TAX_SGSTN": "0.0",
                "GST_TAX_IGSTN": "0.0"
            }
        }

        payload = {
            "json_input": json.dumps([json_input])
        }
        url = 'https://api.ecomexpress.in/apiv2/manifest_awb/'
        return self.request_to_ecom(url, payload, 'POST')
