from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    shipping_email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True
    )


    shipping_full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
        required=True
    )
    shipping_address = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
        required=True
    )
    shipping_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
        required=True
    )
    shipping_postal_code = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'postal code'}),
        required=False
    )
    shipping_state = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}),
        required=True
    )
    shipping_country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}),
        required=True
    )

    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_email',
            'shipping_full_name',
            'shipping_address',
            'shipping_city',
            'shipping_postal_code',
            'shipping_state',
            'shipping_country'
        ]
        exclude = ['user']


class BillingAddressForm(forms.Form):
    card_name =  forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name on card'}),
        required=True
    )
    card_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'card number'}),
        required=True
    )
    cart_expiry_month = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'expiry month'}),
        required=True
    )
    card_cvv = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'cvv'}),
        required=True
    )
    card_adress = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
        required=True
    )
    card_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
        required=True
    )
    card_postal_code = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'postal code'}),
        required=True
    )
    card_country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}),
        required=True
    )