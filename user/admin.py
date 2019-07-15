from django.contrib import admin

# Register your models here.
from . import models


admin.site.register(models.User)
admin.site.register(models.UserActivity)
admin.site.register(models.UserBinding)
admin.site.register(models.UserLog)
