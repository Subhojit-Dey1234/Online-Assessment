from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ExtendedUserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True)
    user_type = models.CharField(max_length=100,null=True,blank=True)
