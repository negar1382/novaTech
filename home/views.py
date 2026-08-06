from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import title

from .models import Category, DealCampaign,Product,Newsletter, SubCategory, Brand, ProductLike
from django.db.models import F, ExpressionWrapper, FloatField
from blog.models import Article
from django.shortcuts import redirect
from cart.models import Cart

# صفحه بندی
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# لایک
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# کامنت
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404, redirect
# ثبت کامنت
from .forms import ProductCommentForm
from django.contrib import messages


def home(request):
    # categories = Category.objects.all()
    campaign = DealCampaign.objects.filter(is_active=True).first()

    amazing_products = (
        Product.objects.filter(stock__gt=0)
        .filter(
            discount_price__isnull=False,
            discount_price__gt=0
        )
        .annotate(
            discount_percent_db=ExpressionWrapper(
                (F("price") - F("discount_price")) * 100.0 / F("price"),
                output_field=FloatField()
            )
        )
        .order_by("-discount_percent_db")[:8]
    )

    newest_products = (
        Product.objects
        .filter(stock__gt=0)
        .order_by("-created_at")[:8]
    )

    popular_products = (
        Product.objects
        .filter(
            stock__gt=0
        )
        .order_by("-likes", "-created_at")[:8]
    )

    articles = Article.objects.filter(is_published=True).order_by("?")[:3]


    context = {
        # "categories": categories,
        'campaign': campaign,
        "amazing_products": amazing_products,
        "newest_products": newest_products,
        "popular_products": popular_products,
        "articles": articles,

    }
    return render(request, "home/home.html", context)



def newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")

        Newsletter.objects.get_or_create(email=email)

    return redirect("/")

def product_list(request, category_id=None, subcategory_id=None, brand_id=None, filter_type=None, brand=None):

    products = Product.objects.filter(
        stock__gt=0
    ).prefetch_related("images")

    title = "همه محصولات"

    if category_id:
        products = products.filter(
            category_id=category_id
        )

        category = Category.objects.get(id=category_id)

        title = category.name

    elif subcategory_id:

        products = products.filter(
            subcategory_id=subcategory_id
        )

        subcategory = SubCategory.objects.get(
            id=subcategory_id
        )

        title = subcategory.name

    elif brand_id:

        products = products.filter(
            brand_id=brand_id
        )

        brand = Brand.objects.get(
            id=brand_id
        )

        title = brand.name

    elif filter_type == "amazing":

        products = (
            products.filter(
                discount_price__isnull=False,
                discount_price__gt=0
            )
            .annotate(
                discount_percent_db=ExpressionWrapper(
                    (F("price") - F("discount_price")) * 100.0 / F("price"),
                    output_field=FloatField()
                )
            )
            .order_by("-discount_percent_db")
        )

        title = "شگفت انگیزها"

    elif filter_type == "popular":

        products = products.filter(likes__gt=0).order_by(
            "-likes",
            "-created_at"
        )

        title = "محبوب‌ترین‌ها"

    elif filter_type == "newest":

        products = products.order_by(
            "-created_at"
        )

        title = "جدیدترین محصولات"

    # برند های محبوب
    if brand:

        # ۱. اگر ورودی یک عدد بود (مثلاً آیدی دیتابیس)

        if str(brand).isdigit():

            products = products.filter(brand_id=int(brand))

            brand_obj = get_object_or_404(Brand, id=int(brand))

            title = f"محصولات برند {brand_obj.name}"


        # ۲. اگر ورودی متن بود (مثلاً 'سامسونگ' یا 'HP')

        else:

            # جستجو بر اساس نام برند در مدل Product

            products = products.filter(brand__name__icontains=brand)

            title = f"محصولات برند {brand}"

    sort = request.GET.get("sort")
    if sort == "cheap":

        products = products.order_by("price")

    elif sort == "expensive":

        products = products.order_by("-price")

    elif sort == "popular":

        products = products.order_by("-likes", "-created_at")

    elif sort == "newest":

        products = products.order_by("-created_at")



    # صفحه بندی
    paginator = Paginator(products, 5)  # هر صفحه ۵ محصول
    page_number = request.GET.get('page', 1)

    try:
        products_page = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        products_page = paginator.get_page(1)

    current_page = products_page.number
    total_pages = paginator.num_pages

    # محاسبه بازه ۵ تایی صفحات
    # نمایش ۵ صفحه حول صفحه فعلی
    start_page = max(1, current_page - 2)
    end_page = min(total_pages, start_page + 4)

    # اگر به انتهای صفحات رسیدیم، بازه رو به سمت چپ تنظیم می‌کنه تا همیشه ۵ شماره دیده بشه
    if end_page - start_page < 4:
        start_page = max(1, end_page - 4)

    page_range = range(start_page, end_page + 1)



    context = {
        "products": products_page,
        "page_range": page_range,
        "total_pages": total_pages,
        "title": title,
        'sort': sort,
        "current_path": request.path,
    }

    return render(
        request,
        "home/product_list/product_list.html",
        context,
    )


# جزئیات محصول
def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug
    )

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    cart_item = None

    liked = False

    if request.user.is_authenticated:
        liked = ProductLike.objects.filter(
            user=request.user,
            product=product
        ).exists()

    comments = product.comments.filter(
        is_approved=True
    )

    if request.user.is_authenticated:

        try:

            cart = request.user.cart

            cart_item = cart.items.filter(
                product=product
            ).first()

        except:

            cart_item = None

    form = ProductCommentForm()
    comments_count = comments.count()

    context = {
        "product": product,
        "related_products": related_products,
        "cart_item": cart_item,
        'liked': liked,
        'comments': comments,
        'form': form,
        'comments_count': comments_count,
    }

    return render(
        request,
        "home/product_detail/product_detail.html",
        context
    )


@login_required
def toggle_product_like(request, product_id):

    if request.method != "POST":
        return JsonResponse({"success": False}, status=400)

    product = get_object_or_404(Product, id=product_id)

    like = ProductLike.objects.filter(
        user=request.user,
        product=product
    ).first()

    if like:
        like.delete()

        if product.likes > 0:
            product.likes -= 1
            product.save()

        liked = False

    else:
        ProductLike.objects.create(
            user=request.user,
            product=product
        )

        product.likes += 1
        product.save()

        liked = True

    return JsonResponse({
        "success": True,
        "liked": liked,
        "likes_count": product.likes
    })



@login_required(login_url="login")
def add_comment(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        form = ProductCommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.user = request.user

            comment.product = product

            comment.save()

            messages.success(
                request,
                "نظر شما با موفقیت ثبت شد و پس از تایید مدیر نمایش داده خواهد شد."
            )

    return redirect(
        "product_detail",
        slug=product.slug
    )