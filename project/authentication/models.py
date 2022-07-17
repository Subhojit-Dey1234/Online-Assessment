from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class ExtendedUserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True)
    user_type = models.CharField(max_length=100,null=True,blank=True)
    otp = models.CharField(max_length=5,null=True,blank=True)


class PhoneOTP(models.Model):
     username = models.CharField(max_length=254, unique=True, blank=True, default=False)
     phone_regex = RegexValidator( regex = r'^\+?1?\d{9,14}$', message = "Phone number must be entered in the form of +919999999999.")
     name = models.CharField(max_length=254, blank=True, null=True)
     phone = models.CharField(validators = [phone_regex], max_length=17)
     otp = models.CharField(max_length=9, blank=True, null=True)
     count = models.IntegerField(default=0, help_text = 'Number of opt_sent')
     validated = models.BooleanField(default=False, help_text= 'if it is true, that means user have validate opt correctly in seconds')

     def __str__(self):
         return str(self.phone) + ' is sent ' + str(self.otp)
