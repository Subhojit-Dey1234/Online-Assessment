import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from twilio.rest import Client, TwilioException
from django.contrib.auth.models import User
from .models import ExtendedUserModel, PhoneOTP
from decouple import config

import string
import random
def id_generator(
    size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
):
    return "".join(random.choice(chars) for _ in range(size))

account_sid = config('account_sid')
auth_token = config('auth_token')
messaging_service_sid = config('messaging_service_sid')

client = Client(account_sid, auth_token) 

def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        return key
    else:
        return False

class ValidatePhoneSendOTP(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone  = str(phone_number)
            print(phone)
            user = ExtendedUserModel.objects.filter(phone_number__iexact = phone)
            print(user)
            if(user.first()):
                user_obj = User.objects.filter(username = user.first().user)
                if False:
                    return Response({
                        'status' : False,
                        'detail' : 'Phone number already exists.'
                        })
                else:
                    key = send_otp(phone)
                    if key:
                        old = PhoneOTP.objects.filter(phone__iexact = phone)
                        if old.exists():
                            user = user_obj.first()
                            old = old.first()
                            old.otp = key
                            user.set_password(str(key))
                            old.validated = False
                            old.save()
                            user.save()
                            txt = f'\nOtp Send for login {key}'
                            try:
                                s_msg = client.messages.create(  
                                    messaging_service_sid = messaging_service_sid, 
                                    body= txt,      
                                    to='+918583891781' 
                                ) 

                                print(s_msg)
                            except TwilioException as e:
                                print(e)
                                return Response("There is a problem with server", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            return Response({
                                'status' : True,
                                'detail' : 'OTP sent successfully.'
                                })
                        else:
                            PhoneOTP.objects.create(
                                username = user.first().user,
                                phone = phone,
                                otp = key,
                                )
                            txt = f'\nOtp Send for login {key}'
                            try:
                                s_msg = client.messages.create(  
                                    messaging_service_sid = messaging_service_sid, 
                                    body= txt,      
                                    to='+918583891781' 
                                ) 

                                print(s_msg)
                            except TwilioException as e:
                                print(e)
                                return Response("There is a problem with server", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            print(s_msg)
                            return Response({
                                'status' : True,
                                'detail' : 'OTP sent successfully.'
                                })
                    else:
                        return Response({
                            'status' : False,
                            'detail' : 'Sending OTP error.'
                            })

            
            else :
                key = send_otp(phone)
                PhoneOTP.objects.create(
                    username = "Random1",
                    phone = phone,
                    otp = key,
                    )
                txt = f'\nOtp Send for login {key}'
                try:
                    s_msg = client.messages.create(  
                        messaging_service_sid = messaging_service_sid, 
                        body= txt,      
                        to='+918583891781' 
                    ) 

                    print(s_msg)
                except TwilioException as e:
                    print(e)
                    return Response("There is a problem with server", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                print(s_msg)
                return Response({
                    'status' : True,
                    'detail' : 'OTP sent successfully.'
                    })
        else:
            return Response({
                'status' : False,
                'detail' : 'Phone number is not given in post request.'
                })

class ValidateOTP(APIView):
    permission_classes = (AllowAny, )


    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone' , False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status' : True,
                        'detail' : 'OTP mactched'
                        })

                else: 
                    return Response({
                        'status' : False,
                        'detail' : 'OTP incorrect.'
                        })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'First proceed via sending otp request.'
                    })
        else:
            return Response({
                'status' : False,
                'detail' : 'Please provide both phone and otp for validations'
                })