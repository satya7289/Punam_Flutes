# Generated by Django 2.2 on 2021-04-26 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_order_courier_tracker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='paypal',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
