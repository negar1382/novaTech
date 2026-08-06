from django import forms
from django.contrib.auth.models import User

# ورود
from django.contrib.auth import authenticate
from .models import UserProfile

# ویرایش
# from django import forms
# from django.contrib.auth.models import User
# from .models import UserProfile


class RegisterPhoneForm(forms.Form):

    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        label="شماره موبایل",
        widget=forms.TextInput(
            attrs={
                "placeholder": "شماره موبایل",
                "autocomplete": "tel",
            }
        )
    )


    def clean_phone_number(self):

        phone = self.cleaned_data["phone_number"]


        if not phone.isdigit():
            raise forms.ValidationError(
                "شماره موبایل فقط باید شامل عدد باشد."
            )


        if not phone.startswith("09"):
            raise forms.ValidationError(
                "شماره موبایل معتبر نیست."
            )


        return phone


class VerifyCodeForm(forms.Form):

    code = forms.CharField(
        max_length=6,
        min_length=6,
        label="کد تایید",
        widget=forms.TextInput(
            attrs={
                "placeholder": "کد ۶ رقمی تایید",
                "autocomplete": "one-time-code",
            }
        )
    )


    def clean_code(self):

        code = self.cleaned_data["code"]


        if not code.isdigit():

            raise forms.ValidationError(
                "کد تایید فقط باید شامل عدد باشد."
            )


        return code




class CompleteRegisterForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                "placeholder": "نام کاربری"
            }
        )
    )


    email = forms.EmailField(
        required=False,
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "ایمیل (اختیاری)"
            }
        )
    )


    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور"
            }
        )
    )


    confirm_password = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "تکرار رمز عبور"
            }
        )
    )


    def clean_username(self):

        username = self.cleaned_data["username"]


        if User.objects.filter(username=username).exists():

            raise forms.ValidationError(
                "این نام کاربری قبلاً استفاده شده است."
            )


        return username



    def clean(self):

        cleaned_data = super().clean()


        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")


        if password and confirm:

            if password != confirm:

                raise forms.ValidationError(
                    "رمز عبور و تکرار آن یکسان نیست."
                )


        return cleaned_data



class LoginForm(forms.Form):

    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                "placeholder": "نام کاربری"
            }
        )
    )


    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور"
            }
        )
    )


    def clean(self):

        cleaned_data = super().clean()


        username = cleaned_data.get("username")
        password = cleaned_data.get("password")


        if username and password:


            user = authenticate(
                username=username,
                password=password
            )


            if user is None:

                raise forms.ValidationError(
                    "نام کاربری یا رمز عبور اشتباه است."
                )


            cleaned_data["user"] = user


        return cleaned_data



class PhoneLoginForm(forms.Form):

    phone_number = forms.CharField(
        max_length=11,
        label="شماره همراه",
        widget=forms.TextInput(
            attrs={
                "placeholder": "شماره همراه"
            }
        )
    )


    def clean_phone_number(self):

        phone = self.cleaned_data["phone_number"]


        if not UserProfile.objects.filter(
            phone_number=phone
        ).exists():

            raise forms.ValidationError(
                "این شماره همراه ثبت نام نکرده است."
            )


        return phone


class PhoneVerifyForm(forms.Form):

    code = forms.CharField(
        max_length=6,
        label="کد تایید",
        widget=forms.TextInput(
            attrs={
                "placeholder": "کد تایید ۶ رقمی"
            }
        )
    )





# ویرایش
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "email": "ایمیل",
        }

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone_number"]

        labels = {
            "phone_number": "شماره همراه",
        }

        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }