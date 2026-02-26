from random import randint
from datetime import timedelta,datetime

def generate_otp():
    return str(randint(100000,999999))

def otp_expiration(minutes=5):
    return datetime.utcnow()+timedelta(minutes=minutes)