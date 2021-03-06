# Generated by Django 2.2 on 2021-04-16 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='coupon_method',
            field=models.CharField(choices=[('percent', 'percent'), ('fixed_amount', 'Fixed Amout')], default='percent', max_length=20),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='coupon_usage_limit',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='coupon_value',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coupon',
            name='coupon_valid',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='coupon_used',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
