from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CompanyRegistrationForm, ProductForm
from .models import Company, CompanyProduct
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def register_company(request):
    """
    Обрабатывает регистрацию компании.

    Если метод запроса POST, создается форма регистрации компании.
    Если форма валидна, создается новый объект компании, связанный с текущим пользователем,
    и происходит перенаправление на панель управления компании.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с формой регистрации компании или перенаправление на панель управления.
    """
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            return redirect('company_dashboard')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'company/register_company.html', {
        'form': form
    })


@login_required
def company_dashboard(request):
    """
    Отображает панель управления компании.

    Загружает данные о компании и ее продуктах, обновляет информацию
    о просмотрах и продажах, а также обрабатывает добавление товара в корзину.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с данными о компании и ее продуктах.
    """
    company = get_object_or_404(Company, user=request.user)
    company_products = CompanyProduct.objects.filter(company=company)

    # Обновляем данные по просмотрам и количеству проданных единиц
    for company_product in company_products:
        product = company_product.product
        company_product.revenue = company_product.quantity_sold * product.get_discounted_price()
        company_product.save()

    # Если запрос POST и связан с добавлением товара в корзину
    if request.method == 'POST' and 'add_to_cart' in request.POST:
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))
        company_product = CompanyProduct.objects.filter(company=company, product_id=product_id).first()
        
        if company_product:
            company_product.quantity_sold += quantity
            company_product.revenue += quantity * company_product.product.get_discounted_price()
            company_product.save()
            return HttpResponseRedirect(reverse('company_dashboard'))

    # Обновляем данные по просмотрам для всех продуктов компании
    for company_product in company_products:
        product = company_product.product
        if request.method == 'GET':
            company_product.views += 1
            company_product.save()

    # Подготовка данных для отображения
    products_data = [
        {
            'id': company_product.product.id,
            'name': company_product.product.name,
            'category': company_product.category.name,
            'views': company_product.views,
            'quantity_sold': company_product.quantity_sold,
            'revenue': company_product.revenue
        }
        for company_product in company_products
    ]

    context = {
        'company': company,
        'products': products_data,
    }
    return render(request, 'company/dashboard.html', context)


@login_required
def add_product(request):
    """
    Обрабатывает добавление нового продукта в компанию.

    Если метод запроса POST, создается форма для добавления продукта.
    Если форма валидна, создается новый объект продукта и связывается с компанией.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с формой добавления продукта или перенаправление на панель управления.
    """
    company = Company.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            CompanyProduct.objects.create(
                company=company,
                product=product,
                category=product.category
            )
            return redirect('company_dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'company/add_product.html', {
        'form': form
    })


@login_required
def edit_product(request, product_id):
    """
    Обрабатывает редактирование существующего продукта.

    Если метод запроса POST, создается форма для редактирования продукта.
    Если форма валидна, изменения сохраняются, и происходит перенаправление на панель управления.

    Args:
        request: HTTP-запрос.
        product_id: ID продукта, который нужно редактировать.

    Returns:
        HttpResponse: HTML-страница с формой редактирования продукта или перенаправление на панель управления.
    """
    company = get_object_or_404(Company, user=request.user)
    company_product = get_object_or_404(CompanyProduct, company=company, product_id=product_id)
    product = company_product.product

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('company_dashboard')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'company_product': company_product,
    }
    return render(request, 'company/edit_product.html', context)


@login_required
def delete_product(request, product_id):
    """
    Обрабатывает удаление продукта из компании.

    Если метод запроса POST, продукт удаляется, и происходит перенаправление на панель управления.

    Args:
        request: HTTP-запрос.
        product_id: ID продукта, который нужно удалить.

    Returns:
        HttpResponse: HTML-страница с подтверждением удаления или перенаправление на панель управления.
    """
    company = get_object_or_404(Company, user=request.user)
    company_product = get_object_or_404(CompanyProduct, company=company, product_id=product_id)
    product = company_product.product

    if request.method == 'POST':
        product.delete()
        return redirect('company_dashboard')
    
    context = {
        'company_product': company_product,
    }
    return render(request, 'company/delete_product.html', context)

