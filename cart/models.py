from django.conf import settings
from django.db import models
from home.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="کاربر"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

    def __str__(self):
        return f"سبد خرید {self.user}"

    @property
    def total_price(self):
        total = 0

        for item in self.items.all():
            total += item.total_price

        return total

    @property
    def total_items(self):
        return self.items.count()

    @property
    def subtotal(self):

        total = 0

        for item in self.items.all():
            total += item.product.price * item.quantity

        return total

    @property
    def total_discount(self):

        total = 0

        for item in self.items.all():

            if item.product.discount_price:
                total += (
                                 item.product.price -
                                 item.product.discount_price
                         ) * item.quantity

        return total

    @property
    def shipping_cost(self):
        if self.total_items == 0:
            return 0
        if self.total_price >= 5000000:
            return 0

        return 100000

    @property
    def final_price(self):

        return self.total_price + self.shipping_cost


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سبد خرید"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="محصول"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="تعداد"
    )

    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ افزودن"
    )

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"

    def __str__(self):
        return self.product.name

    @property
    def total_price(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        return self.product.price * self.quantity