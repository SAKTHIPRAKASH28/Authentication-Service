import os
import smtplib
from fastapi.exceptions import HTTPException
from email.message import EmailMessage
from dotenv import load_dotenv
import string
import secrets
from .cache_handler import *
import ssl
from .db_handler import *

load_dotenv()
password=os.getenv("password")
def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(secrets.choice(characters) for i in range(length))
    return str(otp)

def generate_mail(email,otp):
    msg = EmailMessage()
    msg["Subject"] = "One Time Password"
    msg["To"]=email
    msg["From"]="noreply.lostandfoundtce@gmail.com"
    body = f'Your One Time Password is {otp}'
    msg.set_content(body)
    return msg

def send_email(email):
    exists_email = get_user_creds(email,"email")
    if exists_email:
        raise HTTPException(
                status_code=422, detail="Email Linked with another account")    
    otp=generate_otp()
    add_to_otp_cache(email,otp)
    msg=generate_mail(email,otp)
    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls(context=ssl.create_default_context())
        smtp.login('noreply.lostandfoundtce@gmail.com', password)
        smtp.send_message(msg)
        return {"status":"Email Sent Successfully"}
    except:
        return{"status":"Error. Please check your email id and password"}
    finally:
        smtp.quit()



def validate_otp(email,otp):
    res=get_from_otp_cache(email)[1]
    if not res:
        raise HTTPException(status_code=404,status="OTP EXPIRED")
    else:
        if res!=otp:
            raise HTTPException(status_code=401,detail="Invalid OTP")
        else:
            return True


if __name__=='__main__':
    send_email('sakthiprakash403@gmail.com')
    print(validate_otp('sakthiprakash403@gmail.com',input().strip()))