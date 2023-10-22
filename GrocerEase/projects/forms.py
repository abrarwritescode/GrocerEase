from django.forms import ModelForm
from .models import Customer, Item, Seller, Category
from django import forms
from django.forms import ClearableFileInput

class RegistrationCustomerForm(forms.ModelForm):
    customerpassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['customername', 'customeremail', 'customerpassword', 'customerimage']
        widgets = {
            'customername': forms.TextInput(attrs={'placeholder': 'Enter your name', 'style': 'width: 510px;'}),
            'customeremail': forms.TextInput(attrs={'placeholder': 'Enter your email', 'style': 'width: 510px;'}),
            'customerpassword': forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'style': 'width: 510px;'}),
        }

class LoginCustomerForm(forms.Form):
    customeremail = forms.EmailField()
    customerpassword = forms.CharField(widget=forms.PasswordInput)
    widgets = {
            'customeremail': forms.TextInput(attrs={'placeholder': 'Enter your email', 'style': 'width: 510px;'}),
            'customerpassword': forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'style': 'width: 510px;'}),
        }


class OTPVerificationCustomerForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))


class RegistrationSellerForm(forms.ModelForm):
    sellerpassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Seller
        fields = ['storename', 'selleremail', 'sellerpassword', 'sellerimage']

class LoginSellerForm(forms.Form):
    selleremail = forms.EmailField()
    sellerpassword = forms.CharField(widget=forms.PasswordInput)


class OTPVerificationSellerForm(forms.Form):
    sellerotp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['itemtitle', 'itemprice', 'category', 'itemquantity', 'itemdescription', 'itemfeaturedimage']
        widgets = {
            'itemtitle': forms.TextInput(attrs={'placeholder': 'Input item name here..', 'style': 'width: 510px;'}),
            'itemprice': forms.TextInput(attrs={'placeholder': 'Price', 'style': 'width: 510px;'}),
            'itemquantity': forms.TextInput(attrs={'placeholder': 'Quantity', 'style': 'width: 510px;'}),
            'itemdescription': forms.Textarea(attrs={'placeholder': 'Description', 'style': 'width: 520px; height: 50px;'}),
        }
    

class EditSellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [ 'storename', 'selleremail', 'sellerimage']


class ChangeCustomerImageForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customerimage']
        widgets = {
            'customerimage': forms.FileInput(attrs={'clearable': False}),
        }
