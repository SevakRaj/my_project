from django import forms
from user.models import User
from utils.constants.choices import Roles
from utils.views import is_email
from django.contrib.auth.models import Group
import re
from django.core.validators import RegexValidator


class UserForm(forms.Form):
    first_name = forms.CharField(label="first_name", required=True, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="last_name", required=True, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    mobile = forms.CharField(label="mobile", required=True, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    country_code = forms.CharField(
        label="country_code", required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    role = forms.ChoiceField(label="role", required=True, choices=Roles.choices(
    ), widget=forms.Select(attrs={"class": "form-control form-select"}))
    email = forms.EmailField(label="email", required=True, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    # password = forms.CharField(label="password", required=True, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="password", required=True, widget=forms.PasswordInput(attrs={"class": "form-control"}), validators=[
        RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[\W_])(?=.{8,})\S+$',
            message='Password must be at least 8 characters long, contain at least one uppercase letter, and at least one special character.',
            code='invalid_password'
        )])
    
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),  # Initial queryset is empty
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Groups"
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        self.edit = kwargs.pop("edit", None)
        self.user = kwargs.pop("user", None)

        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = Group.objects.all()
        if self.edit and self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields['mobile'].initial = self.user.mobile
            self.fields["country_code"].initial = self.user.country_code
            self.fields["role"].initial = self.user.role
            self.fields["email"].initial = self.user.email
            # self.fields["password"].initial = self.user.password

            if self.edit:
                self.fields["password"].required = False
                self.fields["password"].widget = forms.HiddenInput()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.user:
            if self.user.email == email:
                return email

        if email != "" and email != None:
            if is_email(email):
                if User.objects.filter(email__iexact=email).exists():
                    raise forms.ValidationError(
                        "User with this email already exist !")
            else:
                raise forms.ValidationError("Your Email wasn't valid !")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if self.user:
            if self.user.mobile == mobile:
                return mobile
        country_code = self.cleaned_data.get('country_code')
        if User.objects.filter(mobile__iexact=mobile).exists():
            raise forms.ValidationError(
                "User with this mobile number already exist !")
        return mobile


class ResetPasswordForm(forms.Form):

    password1 = forms.CharField(required=True, label=("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, label=("Password Confirmation"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        min_length = 8

        if len(password1) < min_length:
            raise forms.ValidationError(
                "Password must be at least 8 characters long")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError(
                "Password must contain at least one special character")

        if not any(char.isupper() for char in password1):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter")

        return password1

