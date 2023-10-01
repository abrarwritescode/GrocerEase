from django.forms import ModelForm
from .models import Customer
from django import forms

class RegistrationForm(forms.ModelForm):
    customerpassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['customername', 'customeremail', 'customerpassword']

class LoginForm(forms.Form):
    customeremail = forms.EmailField()
    customerpassword = forms.CharField(widget=forms.PasswordInput)


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))
