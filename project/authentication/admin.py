from django.contrib import admin

from .models import ExtendedUserModel,PhoneOTP

admin.site.register(ExtendedUserModel)
admin.site.register(PhoneOTP)

# Register your models here.
