from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

class SendEmail:
    def __init__(self, templateName=str, data=dict, subject=str):
        self.template = templateName
        self.data = data
        self.subject = subject
        self.fail_silently=False
    
    def buildHtmlMessage(self, to_list, sender):
        msg_html =  render_to_string(
            self.template, self.data
        )
        return msg_html
        # msg = EmailMessage(subject=self.subject, body=msg_html, from_email=sender, to=to_list)
        # return msg
    
    def send(self, sendMailTo=None, sendMailFrom=None, **kwrgs):
        if not sendMailFrom:
            sendMailFrom = settings.DEFAULT_FROM_EMAIL
        
        # msg = self.buildHtmlMessage(sendMailTo, sendMailFrom)
        # if kwrgs.get('attachments'):
        #     for attachment in kwrgs.get('attachments'):
        #         msg.attach_file(attachment)
        # try:
        #     delivered = msg.send(fail_silently=False)
        #     return delivered
        # except Exception as e:
        #     print("error in email method", e)
        #     return 0
        if sendMailTo:
            send_mail(
                self.subject,
                "",
                sendMailFrom,
                sendMailTo,
                fail_silently=self.fail_silently,
                html_message=self.buildHtmlMessage(sendMailTo, sendMailFrom),
            )
            print(send_mail)
        
        
