# Generated by Django 4.2.4 on 2024-07-25 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='name',
            new_name='user',
        ),
    ]
