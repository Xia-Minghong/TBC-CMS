from django.contrib import admin
from .models import Incident, InciUpdate, Dispatch
# Register your models here.

class IncidentAdmin(admin.ModelAdmin):
    model = Incident
    list_display = ('name', 'status')

admin.site.register(Incident)
admin.site.register(InciUpdate)
admin.site.register(Dispatch)