# Generated by Django 2.2 on 2021-04-22 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StaticData', '0002_countrycurrencyrate'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CountryCurrencyRate',
        ),
    ]