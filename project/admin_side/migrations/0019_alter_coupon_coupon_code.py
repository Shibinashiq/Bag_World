# Generated by Django 4.2.4 on 2023-11-10 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0018_alter_offer_discount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_code',
            field=models.CharField(default='', max_length=255),
        ),
    ]
