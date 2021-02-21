# Generated by Django 2.2 on 2021-02-21 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('image', models.ImageField(upload_to='productImage/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(default='Flute', max_length=200)),
                ('search_tags', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.ManyToManyField(blank=True, to='category.Category')),
                ('images', models.ManyToManyField(blank=True, to='product.ProductImage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CountryCurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('country', models.CharField(blank=True, choices=[['Any', 'Any country'], ['Europe', 'Europe'], ['Asia', 'Asia'], ['Africa', 'Africa'], ['NAmerica', 'North America'], ['SAmerica', 'South America'], ['A_Pacific', 'Asia/Pacific Region'], ['Australia', 'Australia'], ['Austria', 'Austria'], ['Brazil', 'Brazil'], ['Canada', 'Canada'], ['Chile', 'Chile'], ['China', 'China'], ['Egypt', 'Egypt'], ['France', 'France'], ['Georgia', 'Georgia'], ['Germany', 'Germany'], ['Ghana', 'Ghana'], ['Greece', 'Greece'], ['India', 'India'], ['Indonesia', 'Indonesia'], ['Iran', 'Iran'], ['Iraq', 'Iraq'], ['Ireland', 'Ireland'], ['Israel', 'Israel'], ['Italy', 'Italy'], ['Jamaica', 'Jamaica'], ['Japan', 'Japan'], ['Kuwait', 'Kuwait'], ['Malaysia', 'Malaysia'], ['Maldives', 'Maldives'], ['Mexico', 'Mexico'], ['Nepal', 'Nepal'], ['Netherlands', 'Netherlands'], ['New_Zealand', 'New Zealand'], ['Nigeria', 'Nigeria'], ['Oman', 'Oman'], ['Pakistan', 'Pakistan'], ['Paraguay', 'Paraguay'], ['Peru', 'Peru'], ['Philippines', 'Philippines'], ['Poland', 'Poland'], ['Portugal', 'Portugal'], ['Romania', 'Romania'], ['Russia', 'Russia'], ['Saudi_Arabia', 'Saudi Arabia'], ['Singapore', 'Singapore'], ['South_africa', 'South Africa'], ['Spain', 'Spain'], ['Sri Lanka', 'Sri Lanka'], ['Switzerland', 'Switzerland'], ['UAE', 'United Arab Emirates'], ['USA', 'United States of America'], ['UK', 'United Kingdom']], default='', max_length=100, null=True)),
                ('currency', models.CharField(blank=True, choices=[['USD', 'USD'], ['INR', 'INR'], ['EURO', 'EURO'], ['GBP', 'GBP'], ['YEN', 'YEN'], ['CAD', 'CAD'], ['Hong_kong_dollar', 'Hong Kong Dollar'], ['Rubel', 'Rubel'], ['AUD', 'AUD'], ['CNY', 'CNY'], ['Emirates_dhiram', 'Emirates Dirham'], ['Bangladeshi_taka', 'Bangladeshi Taka'], ['Pakistani_rupee', 'Pakistani Rupee']], default='', max_length=30, null=True)),
                ('MRP', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('product', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
            options={
                'verbose_name_plural': 'Country Currencies',
            },
        ),
    ]
