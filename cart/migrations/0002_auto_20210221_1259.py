# Generated by Django 2.2 on 2021-02-21 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipn', '0008_auto_20181128_1032'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ipn.PayPalIPN'),
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
    ]
