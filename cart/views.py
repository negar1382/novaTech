from django.shortcuts import render

# افزودن به سبد خرید
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from home.models import Product
from .models import Cart, CartItem

# افزایش تعداد
from django.views.decorators.http import require_POST

# js
from django.http import JsonResponse
from django.contrib.humanize.templatetags.humanize import intcomma
# افزودن به سبد خرید
from django.urls import reverse

@login_required(login_url="login")
def cart_view(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart
        }
    )


@login_required(login_url="login")
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if product.stock <= 0:

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "message": "این محصول موجود نیست."
            })

        messages.error(
            request,
            "این محصول در حال حاضر موجود نیست."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:

        if cart_item.quantity >= product.stock:

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "message": f"حداکثر {product.stock} عدد موجود است."
                })

            messages.warning(
                request,
                f"حداکثر {product.stock} عدد از این محصول موجود است."
            )

            return redirect(
                "product_detail",
                slug=product.slug
            )

        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return JsonResponse({
            "success": True,
            "quantity": cart_item.quantity,
            "item_id": cart_item.id,
            "cart_count": cart.total_items,

            "increase_url": reverse(
                "increase_quantity",
                args=[cart_item.id]
            ),

            "decrease_url": reverse(
                "decrease_quantity",
                args=[cart_item.id]
            ),
        })

    return redirect(
        "product_detail",
        slug=product.slug
    )


@require_POST
@login_required(login_url="login")
def increase_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        cart = cart_item.cart
        return JsonResponse({
            "success": True,
            "quantity": cart_item.quantity,
            "cart_count": cart_item.cart.total_items,

            "subtotal": intcomma(cart.subtotal),
            "discount": intcomma(cart.total_discount),
            "shipping": "رایگان" if cart.shipping_cost == 0 else f"{intcomma(cart.shipping_cost)} تومان",
            "final_price": intcomma(cart.final_price),
        })

    return redirect(
        request.META.get("HTTP_REFERER", "cart")
    )


@require_POST
@login_required(login_url="login")
def decrease_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    quantity = cart_item.quantity

    if quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

        deleted = False
        quantity = cart_item.quantity

    else:
        cart = cart_item.cart
        cart_item.delete()

        deleted = True
        quantity = 0

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        cart = request.user.cart

        return JsonResponse({
            "success": True,
            "deleted": deleted,
            "quantity": quantity,
            "cart_count": cart.total_items,


            "subtotal": intcomma(cart.subtotal),
            "discount": intcomma(cart.total_discount),
            "shipping": "رایگان" if cart.shipping_cost == 0 else f"{intcomma(cart.shipping_cost)} تومان",
            "final_price": intcomma(cart.final_price),
        })

    return redirect(
        request.META.get("HTTP_REFERER", "cart")
    )




@require_POST
@login_required(login_url="login")
def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart = cart_item.cart

    cart_item.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return JsonResponse({
            "success": True,
            "cart_count": cart.total_items,

            #     اپدیت بدون رفرش خلاصه سفارش

            "subtotal": intcomma(cart.subtotal),
            "discount": intcomma(cart.total_discount),
            "shipping": "رایگان" if cart.shipping_cost == 0 else f"{intcomma(cart.shipping_cost)} تومان",
            "final_price": intcomma(cart.final_price),
        })

    return redirect("cart")