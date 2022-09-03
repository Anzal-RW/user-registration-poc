from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .utils import generate_otp, send_otp


class RegisterView(generics.GenericAPIView):
    '''
    View for user registration.
    Validate input parameters.
    Save user information in database.
    Send email and OTP for verification.
    '''
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])

            # Mobile verification.
            otp = generate_otp()
            user.mobile_otp = otp
            user.save()
            user_mobile = user.mobile
            user_mobile_otp = user.mobile_otp
            send_otp(user_mobile, user_mobile_otp)

            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)