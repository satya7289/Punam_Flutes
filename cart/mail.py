from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class SendEmail:
    def __init__(self, templateName=str, data=dict, subject=str):
        self.template = templateName
        self.data = data
        self.subject = subject
        self.fail_silently=False
    
    def buildHtmlMessage(self):
        return render_to_string(
            self.template, self.data
        )
    
    def send(self, sendMailTo=None, sendMailFrom=None):
        if not sendMailFrom:
            sendMailFrom = settings.DEFAULT_FROM_EMAIL
        if sendMailTo:
            send_mail(
                self.subject,
                "",
                sendMailFrom,
                sendMailTo,
                fail_silently=self.fail_silently,
                html_message=self.buildHtmlMessage(),
            )
