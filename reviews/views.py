from django.shortcuts import get_object_or_404, redirect
from .models import Review, CommentReply
from .forms import ReviewForm
from products.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def add_review(request, product_id):
    """
    Добавляет новый отзыв к продукту.

    Если метод запроса POST и форма валидна, создается новый отзыв
    для указанного продукта, связанный с текущим пользователем.

    Args:
        request: HTTP-запрос.
        product_id: ID продукта, к которому добавляется отзыв.

    Returns:
        HttpResponse: Перенаправление на страницу деталей продукта.
    """
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=product_id)
    return redirect('product_detail', pk=product_id)


@login_required
def reply_to_comment(request, comment_id):
    """
    Добавляет ответ на комментарий отзыва.

    Если метод запроса POST, создается новый ответ на указанный
    комментарий, связанный с текущим пользователем.

    Args:
        request: HTTP-запрос.
        comment_id: ID комментария, на который дается ответ.

    Returns:
        HttpResponse: Перенаправление на страницу деталей продукта.
    """
    comment = get_object_or_404(Review, id=comment_id)
    if request.method == 'POST':
        reply_text = request.POST.get('reply_text')
        CommentReply.objects.create(
            comment=comment,
            user=request.user,
            reply_text=reply_text
        )
    return redirect('product_detail', pk=comment.product.id)

