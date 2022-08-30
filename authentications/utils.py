from django.contrib.sites import requests
from django.core.mail import EmailMessage
from django.http import request
from django.utils.crypto import get_random_string
import requests


def generate_otp():
    '''
    Function to generate otp.
    '''
    return get_random_string(6, '0123456789')


def send_otp(mob, code):
    '''
    Send otp on user's mobile number.
    '''
    print(f'------------->{code} - {mob}<----------------')