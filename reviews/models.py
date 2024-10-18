from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'
    


class CommentReply(models.Model):
    comment = models.ForeignKey('Review', related_name='replies', on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    
