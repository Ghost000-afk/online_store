from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category


class Company(models.Model):
    user = models.OneToOneField(User, related_name='company', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name
    

class CompanyProduct(models.Model):
    company = models.ForeignKey(Company, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.product.name} by {self.company.name}'
    

class CompanyCategory(models.Model):
    company = models.ForeignKey(Company, related_name='categories', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



    def __str__(self):
        return f'{self.category.name} for {self.company.name}'
    
    