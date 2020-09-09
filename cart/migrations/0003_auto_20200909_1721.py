# Generated by Django 2.2 on 2020-09-09 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_auto_20200814_1710'),
        ('cart', '0002_auto_20200909_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(to='product.Product'),
        ),
    ]
