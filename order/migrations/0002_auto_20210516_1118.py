# Generated by Django 2.2 on 2021-05-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='currency',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='currency_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='customization_request',
            field=models.TextField(blank=True, null=True),
        ),
    ]
