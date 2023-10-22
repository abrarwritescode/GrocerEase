from django.forms import ModelForm
from .models import Customer, Item, Seller
from django import forms

class RegistrationCustomerForm(forms.ModelForm):
    customerpassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['customername', 'customeremail', 'customerpassword', 'customerimage']

class LoginCustomerForm(forms.Form):
    customeremail = forms.EmailField()
    customerpassword = forms.CharField(widget=forms.PasswordInput)


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


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['itemtitle', 'itemprice', 'category', 'itemquantity', 'itemdescription', 'itemfeaturedimage']

class EditSellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [ 'storename', 'selleremail']


class ChangeCustomerImageForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customerimage']
        widgets = {
            'customerimage': forms.FileInput(attrs={'clearable': False}),
        }
