# Generated by Django 2.2 on 2021-04-21 15:12

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlideShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('image', models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(bucket='punam-flutes-prods'), upload_to='slideShow/%Y%m%d%M%S')),
                ('alt', models.CharField(blank=True, max_length=1024, null=True)),
                ('heading', models.CharField(blank=True, max_length=1024, null=True)),
                ('description', models.CharField(blank=True, max_length=2048, null=True)),
                ('redirect_link', models.CharField(blank=True, max_length=2048, null=True)),
                ('redirect_link_title', models.CharField(blank=True, max_length=1024, null=True)),
                ('publish', models.BooleanField(blank=True, default=True, null=True)),
                ('order', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ('order', '-created_at'),
            },
        ),
    ]