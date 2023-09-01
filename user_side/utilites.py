from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
import pyotp
from django.core.mail import send_mail




def genarate_otp(email,name):
    totp = pyotp.TOTP(pyotp.random_base32())
    otp = totp.at(0)
    print(otp,'-------------------------------otp-----------------------------')
    # Send OTP via email
    send_mail(
        'Email Verification Code',
        f'Hai {name}, Welcome To NewsHund Your OTP is: {otp}',
        'sender@example.com',
        [email],  # Use user.email instead of undefined email variable
        fail_silently=False,
        )
    return otp