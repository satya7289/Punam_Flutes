# Generated by Django 2.2 on 2021-06-15 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_delete_countrypayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='productquantity',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productquantity',
            name='coupon_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productquantity',
            name='extra',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productquantity',
            name='shipping_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productquantity',
            name='tax_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productquantity',
            name='total_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
