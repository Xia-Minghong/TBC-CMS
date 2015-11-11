from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class ConcreteUserInline(admin.StackedInline):
    model= ConcreteUser
    fk_name = 'user'

class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'is_staff',)
    inlines = [ConcreteUserInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ConcreteUser)


