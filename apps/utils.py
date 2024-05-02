

from django.core.validators import RegexValidator

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


phone_regex = RegexValidator(regex=r'^\d{9,15}$',
                             message="Phone number must be entered in the format: "
                                     "'+9981001010'. Up to 15 digits allowed."
                             )


def send_verification_email(email: str, _uuid: str):
    link = f'http://localhost:8000/api/v1/users/confirm-email/{_uuid}'

    context = {
        'link': link
    }

    html_message = render_to_string('users/email.html', context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject='NewCommerce account activation',
        body=plain_message,
        to=[email]
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()
from django.core.mail import EmailMessage
import os

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
     subject = data['email_subject'], body=data['email_body'], to=[data['to_email']]
    )

    email.send()