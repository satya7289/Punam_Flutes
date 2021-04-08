# Generated by Django 2.2 on 2021-04-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0002_auto_20210316_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='GSTState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('code', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaxRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=200)),
                ('gst_type', models.CharField(blank=True, choices=[['IGST', 'IGST'], ['CGST', 'CGST'], ['SGST', 'SGST']], max_length=10, null=True)),
                ('description', models.TextField()),
                ('country', models.CharField(choices=[['India', 'India'], ['Other', 'Other']], default='', max_length=100, null=True)),
                ('method', models.CharField(choices=[('percent', 'Percent'), ('fixed_amount', 'Fixed Amout')], default='percent', max_length=20)),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('category', models.ManyToManyField(blank=True, to='category.Category')),
                ('state', models.ManyToManyField(blank=True, to='tax_rules.GSTState')),
            ],
        ),
    ]
