# Generated by Django 2.2 on 2021-05-31 05:22

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_testimonial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ('order',)},
        ),
        migrations.RemoveField(
            model_name='blog',
            name='blog_category',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='description',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='display_name',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='menu_item_name',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='sequence',
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_front_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_title',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='image1',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='punam-flutes-prods'), upload_to='blogsImages/%Y%m%d%M%S'),
        ),
        migrations.AddField(
            model_name='blog',
            name='image2',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='punam-flutes-prods'), upload_to='blogsImages/%Y%m%d%M%S'),
        ),
        migrations.AddField(
            model_name='blog',
            name='image3',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='punam-flutes-prods'), upload_to='blogsImages/%Y%m%d%M%S'),
        ),
        migrations.AddField(
            model_name='blog',
            name='image4',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='punam-flutes-prods'), upload_to='blogsImages/%Y%m%d%M%S'),
        ),
        migrations.AddField(
            model_name='blog',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, max_length=1024, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='video1',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='video2',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='video3',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='video4',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='views',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='publish',
            field=models.BooleanField(default=True),
        ),
    ]
