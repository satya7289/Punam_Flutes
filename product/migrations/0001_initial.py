# Generated by Django 2.2 on 2020-05-27 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Flute', max_length=200)),
                ('search_tags', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='category.Category')),
            ],
        ),
    ]
