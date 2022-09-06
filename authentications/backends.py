from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from .models import User

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None):
        try:
            user = User.objects.get(Q(email__iexact=username) | Q(mobile__iexact=username))
            if request.data.get('mobile_otp'):
                if request.data.get('mobile_otp') == user.mobile_otp:
                    return user
            return None
        except User.DoesNotExist:
            return None

        

    def get_user(self, user_id):
        print("USER ID", user_id)
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None