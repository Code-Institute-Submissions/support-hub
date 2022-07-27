from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from .models import CustomUser


# Create custom user creation form
# CREDIT: Pyplane
# URL: https://www.youtube.com/watch?v=1BeZxMbSZNI
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


# Extending the django-allauth Signup Form
# CREDIT: gjbht - GeeksforGeeks
# URL: https://www.geeksforgeeks.org/python-extending-and-customizing-django-allauth/
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    # Set first and last name as required fields for the update form
    # CREDIT: andreaspelme - Stack Overflow
    # URL: https://stackoverflow.com/a/7683392
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
        )


class AdminProfileUpdateForm(ProfileUpdateForm):
    def __init__(self, *args, **kwargs):
        super(AdminProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].disabled = True
        self.fields["last_name"].disabled = True
        self.fields["username"].disabled = True

    class Meta(ProfileUpdateForm):
        model = CustomUser
        fields = ProfileUpdateForm.Meta.fields + (
            "role",
            "team",
        )
