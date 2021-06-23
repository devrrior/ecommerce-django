from django.contrib import admin
from core.users.models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'username', 'first_name')
    list_filter = ('email', 'username', 'first_name', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('email', 'username', 'first_name', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Address)
admin.site.register(Question)
admin.site.register(Answer)
