from django.forms import ModelForm
from .models import Customer, Item, Seller, Category
from django import forms
from django.forms import ClearableFileInput

class RegistrationCustomerForm(forms.ModelForm):
    customerpassword = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegistrationCustomerForm, self).__init__(*args, **kwargs)
        if 'customerpassword' in self.errors:
            self.fields['customerpassword'].widget.attrs['placeholder'] = ''
        else:
            self.fields['customerpassword'].widget.attrs['placeholder'] = 'Enter your password'


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

    def __init__(self, *args, **kwargs):
        super(LoginCustomerForm, self).__init__(*args, **kwargs)
        if 'customerpassword' in self.errors:
            self.fields['customerpassword'].widget.attrs['placeholder'] = ''
        else:
            self.fields['customerpassword'].widget.attrs['placeholder'] = 'Enter your password'

        if 'customeremail' in self.errors:
            self.fields['customeremail'].widget.attrs['placeholder'] = ''
        else:
            self.fields['customeremail'].widget.attrs['placeholder'] = 'Enter your email'



    widgets = {
            'customeremail': forms.TextInput(attrs={'placeholder': 'Enter your email', 'style': 'width: 510px;'}),
            'customerpassword': forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'style': 'width: 510px;'}),
        }


class OTPVerificationCustomerForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))


    
    


class RegistrationSellerForm(forms.ModelForm):
    sellerpassword = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegistrationSellerForm, self).__init__(*args, **kwargs)
        if 'sellerpassword' in self.errors:
            self.fields['sellerpassword'].widget.attrs['placeholder'] = ''
        else:
            self.fields['sellerpassword'].widget.attrs['placeholder'] = 'Enter your password'

    class Meta:
        model = Seller
        fields = ['storename', 'selleremail', 'sellerpassword', 'sellerimage']
        widgets = {
            'storename': forms.TextInput(attrs={'placeholder': 'Enter your name', 'style': 'width: 510px;'}),
            'selleremail': forms.TextInput(attrs={'placeholder': 'Enter your email', 'style': 'width: 510px;'}),
            'sellerpassword': forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'style': 'width: 510px;'}),
        }

class LoginSellerForm(forms.Form):
    selleremail = forms.EmailField()
    sellerpassword = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(LoginSellerForm, self).__init__(*args, **kwargs)
        if 'sellerpassword' in self.errors:
            self.fields['sellerpassword'].widget.attrs['placeholder'] = ''
        else:
            self.fields['sellerpassword'].widget.attrs['placeholder'] = 'Enter your password'

        if 'selleremail' in self.errors:
            self.fields['selleremail'].widget.attrs['placeholder'] = ''
        else:
            self.fields['selleremail'].widget.attrs['placeholder'] = 'Enter your email'
    widgets = {
            'selleremail': forms.TextInput(attrs={'placeholder': 'Enter your email', 'style': 'width: 510px;'}),
            'sellerpassword': forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'style': 'width: 510px;'}),
        }



class OTPVerificationSellerForm(forms.Form):
    sellerotp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['itemtitle', 'category', 'itemquantity', 'itemdescription', 'itemfeaturedimage', 'original_price', 'discount_percentage', 'start_date', 'end_date']
        widgets = {
            'itemtitle': forms.TextInput(attrs={'placeholder': 'Input item name here..', 'style': 'width: 478px;'}),
            'itemquantity': forms.TextInput(attrs={'placeholder': 'Quantity', 'style': 'width: 508px;'}),
            'itemdescription': forms.Textarea(attrs={'placeholder': 'Description', 'style': 'width: 530px; height: 30px;'}),
            'original_price': forms.TextInput(attrs={'placeholder': 'Price', 'style': 'width: 478px;'}),
            'discount_percentage': forms.TextInput(attrs={'placeholder': 'Discount percentage', 'style': 'width: 480px;'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 140px; position: relative; right: 320px; bottom:10px;'}),

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


class ReviewForm(forms.Form):
    rating = forms.IntegerField(
        label='Rating',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'star-rating-input', 'type': 'hidden'}),
    )
    comment = forms.CharField(
        label='Comment',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )
