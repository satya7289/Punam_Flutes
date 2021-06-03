import requests
# from django.conf import settings
from xml.etree import ElementTree


class ECOM:
    def __init__(self, *arg, **kwargs):
        # self.username = settings.ECOM_USERNAME
        # self.password = settings.ECOM_PASSWORD
        self.username = 'punam75136'
        self.password = 'pdgh75dsgh45dghe'

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
    
    def track_order(self, tracking_number='860904701'):
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


        

# ecom = ECOM()
# # print(ecom.check_pincode('854360'))
# print(ecom.track_order())