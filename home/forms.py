from django import forms
from .models import ProductComment


class SendEmailForm(forms.Form):
    subject = forms.CharField(
        label="موضوع",
        max_length=200
    )

    message = forms.CharField(
        label="متن پیام",
        widget=forms.Textarea(attrs={
            "rows": 8
        })
    )


class ProductCommentForm(forms.ModelForm):

    class Meta:

        model = ProductComment

        fields = [
            "text",
        ]

        widgets = {

            "text": forms.Textarea(
                attrs={
                    "placeholder": "نظر خود را درباره این محصول بنویسید...",
                    "rows": 5,
                }
            )

        }