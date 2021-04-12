# Generated by Django 2.2 on 2021-04-12 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_auto_20210316_1756'),
        ('cart', '0005_auto_20210409_0601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='address.Address'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='address.Address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[['Pending', 'Pending'], ['Confirmed', 'Confirmed'], ['Paid', 'Paid'], ['Dispatch', 'Dispatch'], ['Shipped', 'Shipped'], ['Delivered', 'Delivered'], ['Canceled', 'Canceled'], ['Refunded', 'Refunded']], max_length=50, null=True),
        ),
    ]
