# Generated by Django 2.2 on 2021-05-23 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210516_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourrierOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('courrier', models.CharField(blank=True, max_length=255, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=1024, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]