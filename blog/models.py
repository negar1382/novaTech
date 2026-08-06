from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name="عنوان مقاله")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")

    image = models.ImageField(
        upload_to="articles/",
        verbose_name="تصویر مقاله"
    )

    content = RichTextField(
        verbose_name="متن مقاله"
    )

    author = models.CharField(
        max_length=100,
        default="مدیر سایت",
        verbose_name="نویسنده"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="منتشر شود؟"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ انتشار"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)