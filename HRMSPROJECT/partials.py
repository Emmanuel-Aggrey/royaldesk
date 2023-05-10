
import os

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives

EMAIL_FROM = settings.DEFAULT_FROM_EMAIL
import random


class Util:
    @staticmethod
    def send_email(data):
        # email = EmailMessage(
        #   subject=data['subject'],
        #   body=data['body'],
        #   from_email=EMAIL_FROM,
        #   to=[data['to_email']]
        # )
        html_content = body = data['body']
        subject = data['subject']
        msg = EmailMultiAlternatives(
            subject, html_content, EMAIL_FROM, [data['to_email']])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    @staticmethod
    def generated_verification_code():
        return random.randint(10**5, 10**6 - 1)

# GET INITIALS
user= None
department = ''.join([x[0].upper() for x in user.department.name.split(' ')])
