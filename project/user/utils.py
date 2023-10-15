import datetime
import pyotp
from django.core.mail import send_mail

def send_otp(request,email):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.datetime.now() + datetime.timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    print(f"your one time password is  {otp} ")
    
    subject = 'Hello, Django Email! Grab your offer right now '
    message = otp
    from_email = 'otpyour6@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

