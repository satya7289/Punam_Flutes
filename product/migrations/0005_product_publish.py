# Generated by Django 2.2 on 2021-04-13 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20210316_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='publish',
            field=models.BooleanField(default=True),
        ),
    ]
