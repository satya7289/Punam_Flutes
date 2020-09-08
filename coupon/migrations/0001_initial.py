# Generated by Django 2.2 on 2020-05-28 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(max_length=100)),
                ('coupon_code', models.CharField(max_length=20)),
                ('coupon_value', models.IntegerField(default=0)),
                ('coupon_usage_limit', models.IntegerField(default=0)),
                ('coupon_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.Category')),
            ],
        ),
    ]
