# Generated by Django 4.2.4 on 2024-07-31 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_payment_code_alter_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
