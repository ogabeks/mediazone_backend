from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Company)
admin.site.register(models.Group)
admin.site.register(models.Student)