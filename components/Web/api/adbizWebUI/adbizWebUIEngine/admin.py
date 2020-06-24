
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserCreationForm, UserChangeForm
from .models import AdbizUser


class AdbizUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    form = UserChangeForm
    model = AdbizUser

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_staff', 'is_active','is_locked',)
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password', 'dob', 'is_active', "is_locked")}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'dob', 'is_active', 'is_staff', 'is_system_user')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(AdbizUser, AdbizUserAdmin )
