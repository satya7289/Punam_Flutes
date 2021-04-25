# Generated by Django 2.2 on 2021-04-19 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_auto_20210316_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='full_name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='landmark',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(blank=True, choices=[['billing', 'billing'], ['shipping', 'shipping']], default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]