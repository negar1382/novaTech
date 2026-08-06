from django.urls import path
from . import views


urlpatterns = [

    path(
        "checkout/",
        views.checkout_view,
        name="checkout"
    ),
    path(
        "order-success/<int:order_id>/",
        views.order_success,
        name="order_success"
    ),
    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),
    path(
        "my-orders/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

]