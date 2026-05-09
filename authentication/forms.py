from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password'
        })
    )


class SignupForm(forms.Form):

    username = forms.CharField()

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError('Passwords do not match.')

            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', e)

        return cleaned_data


class ResetPasswordForm(forms.Form):

    email = forms.EmailField()

    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit code'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError('Passwords do not match.')

            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', e)

        return cleaned_data
