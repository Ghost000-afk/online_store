from django.contrib import admin
from .models import Company, CompanyCategory, CompanyProduct


admin.site.register(Company)
admin.site.register(CompanyProduct)
admin.site.register(CompanyCategory)


