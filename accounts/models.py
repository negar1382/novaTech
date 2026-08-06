from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="کاربر"
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="شماره همراه"
    )

    is_phone_verified = models.BooleanField(
        default=False,
        verbose_name="تایید شماره همراه"
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل کاربران"


class OTP(models.Model):
    phone_number = models.CharField(
        max_length=11,
        verbose_name="شماره همراه"
    )

    code = models.CharField(
        max_length=6,
        verbose_name="کد تایید"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.phone_number} - {self.code}"

    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = "کدهای تایید"