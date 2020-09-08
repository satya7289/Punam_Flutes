# Generated by Django 2.2 on 2020-08-14 11:40

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20200812_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='image_size',
        ),
        migrations.AddField(
            model_name='productimage',
            name='product_image_5',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='punam-flutes-prods'), upload_to=''),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product_image_6',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='punam-flutes-prods'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='countrycurrency',
            name='country',
            field=models.CharField(blank=True, choices=[['Any', 'Any country'], ['Europe', 'Europe'], ['Asia', 'Asia'], ['Africa', 'Africa'], ['NAmerica', 'North America'], ['SAmerica', 'South America'], ['A_Pacific', 'Asia/Pacific Region'], ['Australia', 'Australia'], ['Austria', 'Austria'], ['Brazil', 'Brazil'], ['Canada', 'Canada'], ['Chile', 'Chile'], ['China', 'China'], ['Egypt', 'Egypt'], ['France', 'France'], ['Georgia', 'Georgia'], ['Germany', 'Germany'], ['Ghana', 'Ghana'], ['Greece', 'Greece'], ['India', 'India'], ['Indonesia', 'Indonesia'], ['Iran', 'Iran'], ['Iraq', 'Iraq'], ['Ireland', 'Ireland'], ['Israel', 'Israel'], ['Italy', 'Italy'], ['Jamaica', 'Jamaica'], ['Japan', 'Japan'], ['Kuwait', 'Kuwait'], ['Malaysia', 'Malaysia'], ['Maldives', 'Maldives'], ['Mexico', 'Mexico'], ['Nepal', 'Nepal'], ['Netherlands', 'Netherlands'], ['New_Zealand', 'New Zealand'], ['Nigeria', 'Nigeria'], ['Oman', 'Oman'], ['Pakistan', 'Pakistan'], ['Paraguay', 'Paraguay'], ['Peru', 'Peru'], ['Philippines', 'Philippines'], ['Poland', 'Poland'], ['Portugal', 'Portugal'], ['Romania', 'Romania'], ['Russia', 'Russia'], ['Saudi_Arabia', 'Saudi Arabia'], ['Singapore', 'Singapore'], ['South_africa', 'South Africa'], ['Spain', 'Spain'], ['Sri Lanka', 'Sri Lanka'], ['Switzerland', 'Switzerland'], ['UAE', 'United Arab Emirates'], ['USA', 'United States of America'], ['UK', 'United Kingdom']], default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='countrycurrency',
            name='currency',
            field=models.CharField(blank=True, choices=[['USD', 'USD'], ['INR', 'INR'], ['EURO', 'EURO'], ['GBP', 'GBP'], ['YEN', 'YEN'], ['CAD', 'CAD'], ['Hong_kong_dollar', 'Hong Kong Dollar'], ['Rubel', 'Rubel'], ['AUD', 'AUD'], ['CNY', 'CNY'], ['Emirates_dhiram', 'Emirates Dirham'], ['Bangladeshi_taka', 'Bangladeshi Taka'], ['Pakistani_rupee', 'Pakistani Rupee']], default='', max_length=30, null=True),
        ),
    ]
