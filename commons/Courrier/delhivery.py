import requests
from django.conf import settings

class Delhivery:
    def __init__(self, *arg, **kwargs):
        test = settings.COURRIER_TEST
        self.api_token = settings.DELHIVERY_API_KEY
        self.api_base_url = "https://staging-express.delhivery.com/api/" if test else "https://track.delhivery.com/c/api/"
    
    # Request to delhivery
    def request_to_delhivery(self, url, payload, method="GET"):
        headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json"
        }
        full_url = self.api_base_url + url
        try:
            if method == "GET":
                response = requests.get(full_url, params=payload, headers=headers)
                return response.status_code, response.json()
            elif method == "POST":
                response = requests.post(full_url, json=payload, headers=headers)
                return response.status_code, response.json()
        except:
            return 500, {"message": "Error", "status": "fail"}
    
    def check_pincode(self, pincode):
        pass
