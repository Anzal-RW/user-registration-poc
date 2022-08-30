from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    # # The forms to add and change user instances
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'mobile', 'first_name')
    list_filter = ('email_verified', 'mobile_verified', 'country')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'mobile', 'country')}
        ),
        ('Verification', {'fields': ('mobile_otp', 'email_verified', 'mobile_verified')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'mobile', 'first_name', 'last_name', 'country',
                )
            }
        ),
    )

    search_fields = ('first_name','mobile')
    ordering = ('first_name',)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)