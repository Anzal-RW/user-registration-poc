import email
from urllib import response
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .utils import generate_otp, send_otp


class RegisterView(GenericAPIView):
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

    
class LoginApiView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        if request.data.get('email'):
            email = request.data.get('email')
            user = authenticate(username=email)

        if request.data.get('mobile'):
            mobile = request.data.get('mobile')
            user = authenticate(request, username=mobile)

        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':'Invalid credentials, try again'}, status=status.HTTP_200_OK)
        
    
