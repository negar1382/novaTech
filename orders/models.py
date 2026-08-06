from django.db import models
from django.conf import settings
from home.models import Product


class Order(models.Model):

    STATUS_CHOICES = (

        ("pending", "در انتظار پرداخت"),

        ("paid", "پرداخت شده"),

        ("processing", "در حال پردازش"),

        ("sent", "ارسال شده"),

        ("completed", "تکمیل شده"),

        ("cancelled", "لغو شده"),

    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="کاربر"
    )


    first_name = models.CharField(
        max_length=100,
        verbose_name="نام"
    )


    last_name = models.CharField(
        max_length=100,
        verbose_name="نام خانوادگی"
    )


    phone = models.CharField(
        max_length=20,
        verbose_name="شماره تماس"
    )

    city = models.CharField(
        max_length=100,
        verbose_name="شهر"
    )

    address = models.TextField(
        verbose_name="آدرس"
    )


    postal_code = models.CharField(
        max_length=20,
        verbose_name="کد پستی"
    )


    total_price = models.PositiveIntegerField(
        verbose_name="مبلغ کل"
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت سفارش"
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت"
    )


    def __str__(self):

        return f"سفارش {self.id} - {self.user}"


class OrderItem(models.Model):


    order = models.ForeignKey(

        Order,

        on_delete=models.CASCADE,

        related_name="items",

        verbose_name="سفارش"

    )


    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE,

        verbose_name="محصول"

    )


    quantity = models.PositiveIntegerField(

        default=1,

        verbose_name="تعداد"

    )


    price = models.PositiveIntegerField(

        verbose_name="قیمت هنگام خرید"

    )


    def total_price(self):

        return self.price * self.quantity


    def __str__(self):

        return self.product.name