from django.shortcuts import render, redirect
from .forms import RegisterPhoneForm
# کد تایید ثبت نام
import random
from datetime import timedelta
from django.utils import timezone
from .models import OTP
from .forms import VerifyCodeForm

# تکمیل ثبت نام
from django.contrib.auth.models import User
from django.contrib.auth import login

from .forms import CompleteRegisterForm
from .models import UserProfile

# خروج
from django.contrib.auth import logout

# ورود
# from django.contrib.auth import login
from .forms import LoginForm

# from .models import OTP, UserProfile
from .forms import PhoneLoginForm, PhoneVerifyForm


# پروفایل
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render


# ویرایش
from .forms import UserForm, UserProfileForm
# پیغام موفقیت ویرایش
from django.contrib import messages


def register_phone(request):

    if request.method == "POST":

        form = RegisterPhoneForm(request.POST)

        if form.is_valid():

            phone = form.cleaned_data["phone_number"]


            code = random.randint(100000, 999999)


            OTP.objects.create(

                phone_number=phone,

                code=str(code),

                expires_at=timezone.now() + timedelta(minutes=2)

            )


            print("================================")
            print("OTP CODE:", code)
            print("PHONE:", phone)
            print("DATABASE OTPs:", OTP.objects.filter(phone_number=phone).values())
            print("================================")


            request.session["register_phone"] = phone


            return redirect("verify_code")


    else:

        form = RegisterPhoneForm()



    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def verify_code(request):

    phone = request.session.get("register_phone")


    if not phone:

        return redirect("register")


    if request.method == "POST":

        form = VerifyCodeForm(request.POST)


        if form.is_valid():

            code = form.cleaned_data["code"]


            otp = OTP.objects.filter(
                phone_number=phone,
                code=code,
                is_used=False
            ).last()


            if otp:


                if otp.expires_at > timezone.now():


                    otp.is_used = True

                    otp.save()


                    print("OTP VERIFIED")


                    return redirect("complete_register")


                else:

                    form.add_error(
                        "code",
                        "کد تایید منقضی شده است."
                    )


            else:

                form.add_error(
                    "code",
                    "کد تایید اشتباه است."
                )


    else:

        form = VerifyCodeForm()


    context = {
            "form": form,
            "phone": phone
        }
    return render(
        request,
        "accounts/verify_code.html",
        context
    )


def complete_register(request):

    phone = request.session.get("register_phone")


    if not phone:

        return redirect("register")



    if request.method == "POST":

        form = CompleteRegisterForm(request.POST)


        if form.is_valid():

            username = form.cleaned_data["username"]

            email = form.cleaned_data["email"]

            password = form.cleaned_data["password"]



            user = User.objects.create_user(

                username=username,

                email=email,

                password=password

            )


            UserProfile.objects.create(

                user=user,

                phone_number=phone,

                is_phone_verified=True

            )


            login(request, user)



            request.session.pop("register_phone", None)



            return redirect("home")



    else:

        form = CompleteRegisterForm()



    return render(
        request,
        "accounts/complete_profile.html",
        {
            "form": form
        }
    )


def logout_view(request):

    logout(request)

    return redirect("home")


def login_view(request):


    if request.method == "POST":


        form = LoginForm(request.POST)


        if form.is_valid():


            user = form.cleaned_data["user"]


            login(
                request,
                user
            )

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("home")



    else:

        form = LoginForm()



    return render(
        request,
        "accounts/login_username.html",
        {
            "form": form
        }
    )


def phone_login(request):


    if request.method == "POST":


        form = PhoneLoginForm(request.POST)


        if form.is_valid():


            phone = form.cleaned_data["phone_number"]



            code = random.randint(
                100000,
                999999
            )



            OTP.objects.create(

                phone_number=phone,

                code=str(code),

                expires_at=timezone.now()
                +
                timedelta(minutes=2)

            )



            print("===================")
            print("LOGIN OTP:", code)
            print("PHONE:", phone)
            print("===================")



            request.session["login_phone"] = phone

            next_url = request.GET.get("next")

            if next_url:
                request.session["next_url"] = next_url
            return redirect("phone_verify")



    else:

        form = PhoneLoginForm()



    return render(
        request,
        "accounts/phone_login.html",
        {
            "form":form
        }
    )


# ورود
def phone_verify(request):

    phone = request.session.get("login_phone")

    if not phone:
        return redirect("phone_login")


    if request.method == "POST":

        form = PhoneVerifyForm(request.POST)

        if form.is_valid():

            code = form.cleaned_data["code"]

            otp = OTP.objects.filter(
                phone_number=phone,
                code=code,
                is_used=False
            ).last()

            if otp and otp.expires_at > timezone.now():

                otp.is_used = True
                otp.save()

                profile = UserProfile.objects.get(
                    phone_number=phone
                )

                login(request, profile.user)

                request.session.pop("login_phone", None)

                next_url = request.session.pop(
                    "next_url",
                    None
                )

                if next_url:
                    return redirect(next_url)

                return redirect("home")

            form.add_error(
                "code",
                "کد تایید اشتباه یا منقضی شده است."
            )

    else:

        form = PhoneVerifyForm()

    return render(
        request,
        "accounts/login_varify.html",
        {
            "form": form
        }
    )




# پروفایل
@login_required
def profile(request):

    context = {
        "user": request.user,
        "active_page": "profile",
    }

    return render(request, "accounts/profile.html", context)


@login_required
def orders(request):
    context = {
        "active_page": "orders",
    }
    return render(request, "accounts/orders.html", context)


@login_required
def account_info(request):

    context = {
        "user": request.user,
        "active_page": "account",
    }

    return render(request, "accounts/account_info.html", context)



# ویرایش
@login_required
def edit_profile(request):

    user_form = UserForm(instance=request.user)

    profile_form, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user_form = UserForm(request.POST, instance=request.user)

        profile_form = UserProfileForm(
            request.POST,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            profile_form.save()

            messages.success(
                request,
                "اطلاعات حساب کاربری با موفقیت ویرایش شد."
            )

            return redirect("account_info")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "active_page": "account",
    }

    return render(
        request,
        "accounts/edite_profile.html",
        context
    )