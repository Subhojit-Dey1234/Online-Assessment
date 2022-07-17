from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
import random
from django.contrib.auth.models import User


from .models import ExtendedUserModel, PhoneOTP

def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        return key
    else:
        return False

class ValidatePhoneSendOTP(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        name = request.data.get('name' , False)
        phone_number = request.data.get('phone')
        if phone_number:
            phone  = str(phone_number)
            user = ExtendedUserModel.objects.filter(phone_number__iexact = phone)
            print(user.first().user)
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
                        return Response({
                            'status' : True,
                            'detail' : 'OTP sent successfully.'
                            })
                    else:
                        PhoneOTP.objects.create(
                            # name = name,
                            phone = phone,
                            otp = key,
                            )
                        return Response({
                            'status' : True,
                            'detail' : 'OTP sent successfully.'
                            })



                else:
                    return Response({
                        'status' : False,
                        'detail' : 'Sending OTP error.'
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
                        'detail' : 'OTP mactched. Please proceed for registration.'
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