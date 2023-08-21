from django.contrib import admin
from . import models


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['name']


# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Company)
admin.site.register(models.Group)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Subscription)
admin.site.register(models.Subject)
