from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class ExtendedUserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number = models.CharField(blank=True,null=True,max_length=100)
    telephone_number = models.CharField(blank=True,null=True,max_length=100)
    user_type = models.CharField(max_length=100,null=True,blank=True)
    father_name = models.CharField(max_length=100,null=True,blank=True)
    aadhar_number = models.CharField(max_length=100,null=True,blank=True)
    street_name = models.CharField(max_length=100,null=True,blank=True)
    city_name = models.CharField(max_length=100,null=True,blank=True)
    state_name = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    zip_code = models.CharField(max_length=100,null=True,blank=True)
    profile = models.ImageField(upload_to = "photos", max_length=254, null = True, blank = True)

    def __str__(self) -> str:
        return self.user.username
