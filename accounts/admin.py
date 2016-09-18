from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User  
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile     
"""用户模块扩展"""
class ProfileInline(admin.StackedInline):
    model = UserProfile
    #fk_name = 'user'
    max_num = 1
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
"""用户模块扩展"""