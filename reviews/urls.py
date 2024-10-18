from django.urls import path
from . import views


urlpatterns = [
    path('add/<int:product_id>/', views.add_review, name='add_review'),
    path('reply/<int:comment_id>/', views.reply_to_comment, name='reply_to_comment')
]