from django.contrib import admin
from .models import *
# ایمیل
from django.urls import path
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import SendEmailForm
from django.contrib import messages

# لایک ها
# from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import ProductLike

# admin.site.register(DealCampaign)
@admin.register(DealCampaign)
class DealCampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "show_end_time", "is_active")

    @admin.display(description="زمان پایان")
    def show_end_time(self, obj):
        return obj.end_time.strftime("%Y-%m-%d %H:%M")



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory')
    search_fields = ('name',)
    list_filter = ('subcategory',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "price")
    ist_filter = ("brand", "subcategory", "category",)
    search_fields = ("name",)
    inlines = [ProductImageInline]
    prepopulated_fields = {"slug": ("name",)}



# ایمیل
@admin.register(Newsletter)
class SubscriberAdmin(admin.ModelAdmin):

    list_display = ("email", "created_at")
    search_fields = ("email",)

    actions = ["send_email_action"]

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "send-email/",
                self.admin_site.admin_view(self.send_email_view),
                name="subscriber_send_email",
            ),
        ]

        return custom_urls + urls

    def send_email_action(self, request, queryset):

        ids = ",".join(str(obj.id) for obj in queryset)

        return redirect(
            f"send-email/?ids={ids}"
        )

    send_email_action.short_description = "ارسال ایمیل"

    def send_email_view(self, request):

        ids = request.GET.get("ids", "")

        subscribers = Newsletter.objects.filter(
            id__in=ids.split(",")
        )

        if request.method == "POST":
            subject = request.POST.get("subject")
            message = request.POST.get("message")

            emails = list(
                subscribers.values_list("email", flat=True)
            )
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                emails,
                fail_silently=False,
            )

            self.message_user(
                request,
                f"ایمیل با موفقیت برای {len(emails)} کاربر ارسال شد.",
                level=messages.SUCCESS,
            )

            return redirect("..")
        else:

            form = SendEmailForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "ارسال ایمیل",
            "form": form,
            "subscribers": subscribers,
        }

        return render(
            request,
            "home/admin/send_email.html",
            context,
        )


# لایک
class ProductLikeInline(admin.TabularInline):
    model = ProductLike
    extra = 0
    can_delete = False
    verbose_name = "محصول لایک شده"
    verbose_name_plural = "محصولات لایک شده"

    fields = ("product", "created_at")
    readonly_fields = ("product", "created_at")

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    inlines = [ProductLikeInline]

    fieldsets = (
        (None, {
            "fields": (
                "username",
                "password",
            )
        }),

        ("اطلاعات شخصی", {
            "fields": (
                "first_name",
                "last_name",
                "email",
            )
        }),

        ("دسترسی‌ها", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
            )
        }),

        ("تاریخ‌ها", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )


# کامنت
@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "product",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "is_approved",
    )

    search_fields = (
        "user__username",
        "product__name",
        "text",
    )