from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product


@login_required
def view_cart(request):
    """
    Отображает содержимое корзины пользователя.

    Если корзина не существует, она создается автоматически.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с содержимым корзины.
    """
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, pk):
    """
    Добавляет товар в корзину.

    Если товар уже находится в корзине, увеличивает его количество.

    Args:
        request: HTTP-запрос.
        pk: ID товара, который нужно добавить в корзину.

    Returns:
        HttpResponseRedirect: Перенаправление на страницу корзины.
    """
    product = get_object_or_404(Product, id=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


@login_required
def remove_from_cart(pk):
    """
    Удаляет товар из корзины.

    Args:
        pk: ID товара, который нужно удалить из корзины.

    Returns:
        HttpResponseRedirect: Перенаправление на страницу корзины.
    """
    cart_item = get_object_or_404(CartItem, id=pk)
    cart_item.delete()
    return redirect('view_cart')



