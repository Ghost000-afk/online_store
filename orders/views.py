import uuid
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import stripe

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.models import Cart
from company.models import CompanyProduct


import uuid

def generate_payment_code():
    """
    Генерирует уникальный код для платежа.

    Returns:
        str: Уникальный код платежа в виде строки.
    """
    return str(uuid.uuid4())


@login_required
def create_order(request):
    """
    Обрабатывает создание нового заказа.

    Если метод запроса POST и форма валидна, создается новый заказ,
    заполняется информация о заказанных товарах, обновляются данные
    о проданных товарах и производится перенаправление на страницу
    обработки платежа или наличного расчета.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с формой создания заказа или перенаправление.
    """
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            cart = Cart.objects.get(user=request.user)
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                # Обновление данных CompanyProduct, если он существует для данного продукта
                company_product = CompanyProduct.objects.filter(product=item.product).first()
                if company_product:
                    company_product.quantity_sold += item.quantity
                    company_product.revenue += item.quantity * item.product.get_discounted_price()
                    company_product.save()

            cart.items.all().delete()

            if order.payment_method == 'credit_card':
                return redirect('process_payment', order_id=order.id)
            else:
                order.payment_code = generate_payment_code()
                order.save()
                return redirect('cash_on_delivery', order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create_order.html', {'form': form})


@login_required
def order_list(request):
    """
    Отображает список заказов текущего пользователя.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница со списком заказов.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    """
    Отображает детали конкретного заказа.

    Args:
        request: HTTP-запрос.
        pk: ID заказа.

    Returns:
        HttpResponse: HTML-страница с деталями заказа.
    """
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def process_payment(request, order_id):
    """
    Обрабатывает платеж для заказа через платежную систему.

    Если метод запроса POST, производится попытка создания платежа.
    Если платеж успешен, статус заказа обновляется на 'Completed'.

    Args:
        request: HTTP-запрос.
        order_id: ID заказа, для которого производится платеж.

    Returns:
        HttpResponse: HTML-страница для обработки платежа или перенаправление.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        try:
            charge = stripe.Charge.create(
                amount=int(order.get_total() * 100),
                currency='usd',
                description=f'Order {order.id}',
                source=request.POST['stripeToken'],
            )
            order.status = 'Completed'
            order.save()
            return redirect('order_list')
        except stripe.error.StripeError:
            return redirect('payment_error')
    else:
        return render(request, 'orders/payment.html', {
            'order': order,
            'amount': order.get_total(),
            'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY
        })


@login_required
def cash_on_delivery(request, order_id):
    """
    Обрабатывает заказ с наличным расчетом.

    Если метод запроса POST, генерируется уникальный код платежа и статус
    заказа обновляется на 'Pending'.

    Args:
        request: HTTP-запрос.
        order_id: ID заказа.

    Returns:
        HttpResponse: HTML-страница с информацией о заказе и уникальным кодом платежа.
    """
    order = get_object_or_404(Order, id=order_id)
    unique_payment_code = f'COD--{order.id}--{order.created_at.strftime("%Y%m%d%H%M%S")}'
    if request.method == 'POST':
        order.payment_code = unique_payment_code
        order.status = 'Pending'
        order.save()
        return redirect('order_list')

    return render(request, 'orders/cash_on_delivery.html', {
        'order': order,
        'unique_payment_code': unique_payment_code
    })


def payment_error(request):
    """
    Отображает страницу с ошибкой платежа.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с информацией об ошибке платежа.
    """
    return render(request, 'orders/payment_error.html')

