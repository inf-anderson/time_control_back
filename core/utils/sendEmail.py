from django.core.mail import EmailMessage


def send_email(subject, message, email):
    email = EmailMessage(subject, message, to=[email])
    email.send()
    return email
