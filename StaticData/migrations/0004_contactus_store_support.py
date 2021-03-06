# Generated by Django 2.2 on 2021-04-24 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StaticData', '0003_delete_countrycurrencyrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('display_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('publish', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('display_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('store_type', models.CharField(blank=True, choices=[['Indian Stores', 'Indian Stores'], ['International Stores', 'International Stores']], max_length=100, null=True)),
                ('first_description', models.TextField(blank=True, null=True)),
                ('main_description', models.TextField(blank=True, null=True)),
                ('publish', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ('store_type', 'order'),
            },
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('display_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('first_description', models.TextField(blank=True, null=True)),
                ('main_description', models.TextField(blank=True, null=True)),
                ('link', models.CharField(blank=True, max_length=1024, null=True)),
                ('publish', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ('display_name', 'order'),
            },
        ),
    ]
