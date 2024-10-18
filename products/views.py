from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from reviews.forms import ReviewForm


def category_list(request):
    """
    Отображает список всех категорий товаров.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница со списком категорий.
    """
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {
        'categories': categories
    })


def product_list(request, category_id):
    """
    Отображает список товаров в выбранной категории.

    Args:
        request: HTTP-запрос.
        category_id: ID категории для отображения товаров.

    Returns:
        HttpResponse: HTML-страница со списком товаров в категории.
    """
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'products/product_list.html', {
        'category': category,
        'products': products
    })


def product_detail(request, pk):
    """
    Отображает детальную информацию о товаре.

    Args:
        request: HTTP-запрос.
        pk: ID товара для отображения.

    Returns:
        HttpResponse: HTML-страница с информацией о товаре и формой отзыва.
    """
    product = get_object_or_404(Product, id=pk)
    review_form = ReviewForm()
    return render(request, 'products/product_detail.html', {'product': product, 'review_form': review_form})


def search_products(request):
    """
    Ищет товары по запросу.

    Args:
        request: HTTP-запрос, содержащий строку поиска.

    Returns:
        HttpResponse: HTML-страница с результатами поиска товаров.
    """
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'products/search_results.html', {
        'products': products,
        'query': query
    })



