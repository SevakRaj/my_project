import os
import magic

# import code128
# from PIL import Image, ImageDraw, ImageFont

from random import randint, choices

from django.utils import timezone
from django.shortcuts import render, redirect
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.validators import validate_email, ValidationError
from django.views.generic import View
from django.http import JsonResponse
from django.utils.encoding import force_bytes, force_str #force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.files.storage import default_storage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Max


# Token Generator
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(
            microsecond=0, tzinfo=None)
        return str(user.pk) + user.password + str(login_timestamp) + str(timestamp)
    

account_activation_token = TokenGenerator()

# Create your views here.

def default_due_date():
    return now() + timedelta(days=7)


# function to generate OTP
def generate_otp():
    otp = ""
    for _ in range(4):
        otp += str(randint(1, 9))
    return otp

# Email validate
def is_email(string):
    try:
        validate_email(string)
        return True
    except ValidationError:
        return False


# set secured url
def get_secured_url(request):
    if request.is_secure():
        return "https://"
    else:
        return "http://"


# Not able to User verification due to Error : EmailMessage.__init__() got an unexpected keyword argument 'html_message'
def send_email(obj, message, template, request, email_subject=None, to_email=None, attachment_path=None):
    message.update({
        "domain": get_secured_url(request) + request.META["HTTP_HOST"]
    })
    
    # Render the email content from the template
    email_message = render_to_string("email/" + template, message)

    if to_email:
        from_email=to_email
    else:
        from_email= settings.DEFAULT_FROM_EMAIL
    
    if email_subject:
        subject = email_subject
    else:
        subject = settings.EMAIL_WELCOME_MESSAGE

    # Create an EmailMessage object
    email = EmailMultiAlternatives(
        to= [to_email], #[obj.email],
        from_email= from_email,
        subject = subject,
    )
    email.attach_alternative(email_message,"text/html")

    # Attach a file to the email if attachment_path is provided
    if attachment_path:
        with open(attachment_path, 'rb') as file:
            email.attach_file(attachment_path)

    # Send the email
    email.send()



# decode data
def decode_data(input_data):
    uid = force_str(urlsafe_base64_decode(input_data))
    return uid


# encode data
def encode_data(input_data):
    uid = urlsafe_base64_encode(force_bytes(input_data))
    return uid


# Send OTP function
def send_otp(obj, retry=None):
    otp = generate_otp()
    obj.otp = otp
    obj.otp_created_at = timezone.now()
    obj.save()
    # mobile_number = obj.mobile
    # sms_message = "Your OTP to login with Zewellers is " + otp + \
        # ". Valid for 30 minutes. Never share your OTP with anyone. - Thanks, Zewellers Team"
    # result = send_sms(sms_message, mobile_number, retry)
    return {'ErrorCode':'000'}

def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'        

#upload file
def upload_file(instance, filename, dir_name):
    name = filename.name.replace(" ", "_")
    url = "%s/%d/%s" % (dir_name,int(instance.id), name)
    file_name = default_storage.save(url, filename)
    return file_name

    

def send_email_with_attachment(subject, message, from_email, recipient_list, attachment_path):
    with open(attachment_path, 'rb') as file:
        file_content = file.read()

    mime_type = magic.from_buffer(file_content, mime=True)

    # Extract the filename from the attachment_path
    file_name = os.path.basename(attachment_path)

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(file_name, file_content, mime_type)

    # Send the email
    email.send()


# function for pagination
# def pagination_offsets(count, page=settings.PAGE, page_size=settings.PAGE_SIZE):
#     if page == 1:
#         start_offset = 0
#         end_offset = page * page_size
#         next_page = page + 1
#         previous_page = None
#     else:
#         start_offset = (page - 1) * page_size
#         end_offset = page * page_size

#     if end_offset >= count:
#         end_offset = count
#         next_page = None
#         previous_page = page - 1
#     else:
#         next_page = page + 1
#         previous_page = page - 1

#     next_page = None if next_page == 0 else next_page
#     previous_page = None if previous_page == 0 else previous_page

#     return start_offset, end_offset, next_page, previous_page

