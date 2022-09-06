import email
from urllib import response
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer, LoginSerializer, GenLoginOTPSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from .models import User
from .utils import generate_otp, send_otp, Util
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


class AuthUserApiView(GenericAPIView):
    '''
    view for berear token
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response({'user':serializer.data})


class RegisterView(GenericAPIView):
    '''
    View for user registration.
    Validate input parameters.
    Save user information in database.
    Send OTP on mobile.
    '''
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])

            # generate otp
            otp = generate_otp()
            user.mobile_otp = otp
            user.save()

            user_mobile = user.mobile
            user_mobile_otp = user.mobile_otp
            send_otp(user_mobile, user_mobile_otp)

            user_name = f'{user.first_name} {user.last_name}'
            email_body = 'Hi '+ user_name +', \n Your OTP for login is\n' + user_mobile_otp
            data = {
                'email_body': email_body,
                'email_to':user.email, 
                'email_subject':'Verify OTP',
                }
            Util.send_email(data)

            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(GenericAPIView):

    REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authentications.jwt.JWTAuthentication',
    ]}
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
            # current time - otp validation time <= otp generated time.
            if timezone.now()-timedelta(hours=0.05) <= user.otp_generated_at:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'otp':'OTP has expired'}, status=status.HTTP_410_GONE)
        return Response({'message':'Invalid credentials, try again'}, status=status.HTTP_401_UNAUTHORIZED)


class GenLoginOTPApiView(GenericAPIView):
    '''
    View to generate otp
    Generate otp
    Send otp
    '''

    serializer_class = GenLoginOTPSerializer

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_data = serializer.data
            print(user_data)

            try:
                user = User.objects.get(mobile=user_data['mobile'])

                otp = generate_otp()
                user.mobile_otp = otp
                user.save()

                user_mobile = user.mobile
                user_mobile_otp = user.mobile_otp
                send_otp(user_mobile, user_mobile_otp)
                print(serializer.data)

                # user_name = f'{user.first_name} {user.last_name}'
                # email_body = 'Hi '+ user_name +', \n Your OTP for login is\n' + user_mobile_otp
                # data = {
                #     'email_body': email_body,
                #     'email_to':user.email,
                #     'email_subject':'Verify OTP',
                #     }
                # Util.send_email(data)

                return Response(serializer.data, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({'error':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)