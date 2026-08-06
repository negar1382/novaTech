from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CheckoutForm
from .models import Order, OrderItem

from django.shortcuts import get_object_or_404

# سفارش های من
# from django.contrib.auth.decorators import login_required
# from .models import Order


@login_required(login_url="login")
def checkout_view(request):

    cart = request.user.cart


    if cart.total_items == 0:

        return redirect("cart")


    if request.method == "POST":

        form = CheckoutForm(request.POST)


        if form.is_valid():

            order = form.save(commit=False)


            order.user = request.user


            order.total_price = cart.final_price


            order.save()



            for item in cart.items.all():

                OrderItem.objects.create(

                    order=order,

                    product=item.product,

                    quantity=item.quantity,

                    price=(
                        item.product.discount_price
                        if item.product.discount_price
                        else item.product.price
                    )

                )


            cart.items.all().delete()


            return redirect(
                "order_success",
                order_id=order.id
            )




    else:

        form = CheckoutForm(

            initial={

                "first_name": request.user.first_name,

                "last_name": request.user.last_name,

                "phone": request.user.profile.phone_number,
            }

        )



    return render(
        request,
        "orders/checkout.html",
        {
            "cart": cart,
            "form": form
        }
    )




@login_required(login_url="login")
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )


    return render(
        request,
        "orders/order_success.html",
        {
            "order": order
        }
    )




@login_required(login_url="login")
def my_orders(request):
    print("Current User:", request.user)
    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )


    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )


@login_required(login_url="login")
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    status_step = {
        "pending": 1,
        "paid": 1,
        "processing": 2,
        "sent": 3,
        "completed": 4,
        "cancelled": 0,
    }

    context = {
        "order": order,
        "status_step": status_step.get(order.status, 0),
    }

    return render(
        request,
        "orders/order_detail.html",
        context
    )