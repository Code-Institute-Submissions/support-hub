from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm


# Register CustomUserCreationForm and display Roles as an additional fieldset
# CREDIT: Pyplane
# URL: https://www.youtube.com/watch?v=1BeZxMbSZNI
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        ("Role and Team", {"fields": ("role", "team")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
