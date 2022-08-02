"""Admin for accounts application"""


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import CustomUser


# CREDIT: Pyplane
# URL: https://www.youtube.com/watch?v=1BeZxMbSZNI
class CustomUserAdmin(UserAdmin):
    """Set additional fieldset to display on the change user page of the admin
    portal.
    """

    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        ("Role and Team", {"fields": ("role", "team")}),
    )

    list_display = (
        "username",
        "id",
        "email",
        "full_name",
        "is_staff",
        "role",
    )

    ordering = "id",


# register models with admin site so they can be managed
admin.site.register(CustomUser, CustomUserAdmin)
