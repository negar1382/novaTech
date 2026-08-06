from .models import Cart


def cart_context(request):

    cart = None

    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

    return {
        "cart": cart
    }