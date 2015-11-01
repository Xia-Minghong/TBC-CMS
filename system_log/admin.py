from django.contrib import admin
import system_log.models

# Register your models here.
admin.site.register(system_log.models.Syslog)