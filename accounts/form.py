from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': 'Enter a valid email address.',  # override default
            'required': 'Email is required.'
        }
    )

    def clean_email(self):
        demail = self.cleaned_data.get('email', '').strip().lower()
        allowed_domains = ['srkrec.ac.in', 'gmail.com']
        if '@' not in demail:
            raise forms.ValidationError("Enter a valid email address.")
        domain = demail.split('@')[-1]
        if domain not in allowed_domains:
            raise forms.ValidationError("Email must be from srkrec.ac.in or Gmail.")
        return demail

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
