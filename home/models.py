from django.db import models

# لایک
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    icon_class = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="subcategories", verbose_name="دسته")
    name = models.CharField(max_length=100, verbose_name="نام")

    def __str__(self):
        return self.name


class Brand(models.Model):
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name="brands", verbose_name="زیر دسته")
    name = models.CharField(max_length=100, verbose_name="نام")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="دسته بندی")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products", verbose_name="زیر دسته", blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name="products", verbose_name="نوع محصول", blank=True, null=True)
    description = models.TextField( verbose_name="توضیحات")
    price = models.PositiveIntegerField( verbose_name="قیمت")
    discount_price = models.PositiveIntegerField(null=True, blank=True, verbose_name="قیمت با تخفیف")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    likes = models.PositiveIntegerField(default=0, verbose_name="تعداد لایک")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.discount_price:
            return int(
                (self.price - self.discount_price)
                / self.price * 100
            )
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="محصول")
    image = models.ImageField(upload_to="products/", verbose_name="تصویر")

    def __str__(self):
        return f"{self.product.name}"


class ProductLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="liked_products",
        verbose_name="کاربر"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="liked_users",
        verbose_name="محصول"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان لایک"
    )

    class Meta:
        verbose_name = "لایک محصول"
        verbose_name_plural = "لایک محصولات"
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class ProductComment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="کاربر"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="محصول"
    )

    text = models.TextField(
        verbose_name="متن دیدگاه"
    )

    is_approved = models.BooleanField(
        default=False,
        verbose_name="تایید شده"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت"
    )


    class Meta:
        verbose_name = "دیدگاه محصول"
        verbose_name_plural = "دیدگاه محصولات"
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.user.username} - {self.product.name}"



class DealCampaign(models.Model):
    title = models.CharField(max_length=100, default="شگفت‌انگیزها")
    end_time = models.DateTimeField(verbose_name="زمان پایان تخفیف")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")

    def __str__(self):
        return self.email

    # class Meta:
    #     verbose_name = "عضو خبرنامه"
    #     verbose_name_plural = "اعضای خبرنامه"