from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path( "newsletter/", views.newsletter, name="newsletter"),

    path(
        "products/",
        views.product_list,
        name="product_list",
    ),

    path(
            "products/category/<int:category_id>/",
            views.product_list,
            name="category_products",
        ),

        path(
            "products/subcategory/<int:subcategory_id>/",
            views.product_list,
            name="subcategory_products",
        ),

        path(
            "products/brand/<int:brand_id>/",
            views.product_list,
            name="brand_products",
        ),

    path(
        "products/amazing/",
        views.product_list,
        {"filter_type": "amazing"},
        name="amazing_products",
    ),

    path(
        "products/popular/",
        views.product_list,
        {"filter_type": "popular"},
        name="popular_products",
    ),

    path(
        "products/newest/",
        views.product_list,
        {"filter_type": "newest"},
        name="newest_products",
    ),

    path('products/brand/<str:brand>/', views.product_list, name='brand_products'),
    path(
        "products/<slug:slug>/",
        views.product_detail,
        name="product_detail"
    ),
    path(
        "products/<int:product_id>/like/",
        views.toggle_product_like,
        name="toggle_product_like",
    ),
    path(
        "products/<int:product_id>/comment/",
        views.add_comment,
        name="add_comment",
    ),
]
