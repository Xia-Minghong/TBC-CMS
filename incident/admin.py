from django.contrib import admin
from .models import Incident
# Register your models here.

class IncidentAdmin(admin.ModelAdmin):
    model = Incident
    list_display = ('name', 'status')

admin.site.register(Incident)