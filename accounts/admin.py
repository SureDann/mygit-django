from django.contrib import admin
from . import models

admin.site.register(models.UserS)
admin.site.register(models.UserRefreshToken)
# Register your models here.
