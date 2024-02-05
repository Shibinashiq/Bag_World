# Generated by Django 5.0.1 on 2024-02-02 10:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0021_coupon_min_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='end_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='coupon',
            name='start_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
