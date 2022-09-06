from lib2to3.pytree import Base
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
import jwt
from .models import User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # get header
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(' ')

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed('Token not valid')

        token = auth_token[1]

        # decode token to get user because according to docs we need to return user
        # link to doc:
        # https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
            email = payload['email']
            user = User.objects.get(email=email)
            return (user, token) 

        # exceptional handling for line 26
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('Token is expired, login again')

        # exceptional handling for line 26
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed('Token is invalid')

        # exceptional handling for line 30
        except jwt.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed('No such user')