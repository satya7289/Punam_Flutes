# Generated by Django 2.2 on 2021-04-09 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax_rules', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gststate',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='gststate',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
