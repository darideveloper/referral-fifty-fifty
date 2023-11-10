from referralfiftyfifty.settings import EMAIL_HOST_USER
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def submit_email (subject:str, html_content:str, email:str): 
    # activation_link = f"{HOST}/activate/{user.hash}"
        
    # html_content = f'<p>Click here to complete your registration: <a href="{activation_link}"> {activation_link}</p>'
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        EMAIL_HOST_USER,
        [email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()