import requests
from django.conf import settings


class sendSMS:
    # mobile and type are required paramter
    def __init__(self, mobile='', type='', *args, **kwargs):
        self.configure()
        self.mobile = mobile
        self.type = type
        self.args = args
        self.kwargs = kwargs

    def configure(self):
        # configure the credentials
        mysmszone_url = 'http://sms.mysmszone.in/'
        api_version = 'api_v2/'
        path = 'message/send'
        self.base_url = mysmszone_url + api_version + path
        self.sender_id = 'BASURI'
        self.api_key = settings.SMS_API_KEY
        self.to_Send = settings.SEND_SMS

    # call this method to send sms
    def send(self):
        if self.mobile == '':
            return False
        if self.type == 'otp':
            otp = self.kwargs.get('OTP')
            if otp:
                return self.OTP(otp)
            return False
        elif self.type == 'order_placed':
            return self.OrderPlaced()
        elif self.type == 'order_cancelled':
            return self.OrderCancelled()
        elif self.type == 'order_shipped':
            return self.OrderShipped()
        elif self.type == 'order_refunded':
            return self.OrderRefunded()
        elif self.type == 'order_delivered':
            return self.OrderDelivered()
        return False

    def send_sms(self, message, dlt_template_id):
        params = {
            'api_key': self.api_key,
            'sender_id': self.sender_id,
            'dlt_template_id': dlt_template_id,
            'mobile_no': self.mobile,
            'message': message,
        }
        # print(self.base_url, params)
        if self.to_Send:
            try:
                req = requests.get(self.base_url, params=params)
                if req.status_code == 200:
                    return True
            except:
                pass
        print(message)
        return False

    def OTP(self, otp):
        message = f'{otp} is your Punam Flutes OTP. Do not share it with anyone. Thanks'
        dlt_template_id = '1207161915134996407'
        return self.send_sms(message, dlt_template_id)

    def OrderPlaced(self,):
        message = ''
        dlt_template_id = ''
        return self.send_sms(message, dlt_template_id)

    def OrderShipped(self,):
        message = ''
        dlt_template_id = ''
        return self.send_sms(message, dlt_template_id)

    def OrderCancelled(self,):
        message = ''
        dlt_template_id = ''
        return self.send_sms(message, dlt_template_id)

    def OrderDelivered(self,):
        message = 'Your Punam Flutes order has been delivered. Please contact us if you have any queries.'
        dlt_template_id = '1207161917005451759'
        return self.send_sms(message, dlt_template_id)

    def OrderRefunded(self,):
        message = ''
        dlt_template_id = ''
        return self.send_sms(message, dlt_template_id)
