from django import forms
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name', required=True)
    email = forms.EmailField(label='Email', required=True)
    message = forms.CharField(label='Message', required=True)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='username_form', required=True)
    email = forms.EmailField(max_length=100, label='email_form', required=True)
    password = forms.CharField(max_length=100, label='password_form', required=True)
    confirm_password = forms.CharField(max_length=100, label='confirm_password_form', required=True)

    # make a connection between register form and auth_user table(prebuilt)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password does not match!!!")