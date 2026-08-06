from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = [
            "first_name",
            "last_name",
            "phone",
            "city",
            "address",
            "postal_code",
        ]


        labels = {

            "first_name": "نام",

            "last_name": "نام خانوادگی",

            "phone": "شماره همراه",

            "city": "شهر",

            "address": "آدرس کامل",

            "postal_code": "کد پستی",

        }


        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class": "checkout-input"
                }
            ),


            "last_name": forms.TextInput(
                attrs={
                    "class": "checkout-input"
                }
            ),


            "phone": forms.TextInput(
                attrs={
                    "class": "checkout-input"
                }
            ),


            "city": forms.TextInput(
                attrs={
                    "class": "checkout-input"
                }
            ),


            "address": forms.Textarea(
                attrs={
                    "class": "checkout-input",
                    "rows": 4
                }
            ),


            "postal_code": forms.TextInput(
                attrs={
                    "class": "checkout-input"
                }
            ),

        }