from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class OperatorInline(admin.StackedInline):
    model= Operator
    fk_name = 'user'

class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'is_staff',)
    inlines = [OperatorInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Operator)
admin.site.register(KeyDecisionMaker)
admin.site.register(CrisisManager)
