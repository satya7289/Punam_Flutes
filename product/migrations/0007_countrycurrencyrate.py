# Generated by Django 2.2 on 2021-04-22 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20210416_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryCurrencyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('country', models.CharField(blank=True, max_length=1024, null=True)),
                ('alpha_2_code', models.CharField(blank=True, max_length=20, null=True)),
                ('alpha_3_code', models.CharField(blank=True, max_length=20, null=True)),
                ('numeric_code', models.CharField(blank=True, max_length=20, null=True)),
                ('currency', models.CharField(blank=True, max_length=1024, null=True)),
                ('currency_code', models.CharField(blank=True, max_length=20, null=True)),
                ('currency_symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('currency_rate', models.FloatField(blank=True, null=True)),
                ('base', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'ordering': ('country',),
            },
        ),
    ]