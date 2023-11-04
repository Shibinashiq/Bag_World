# Generated by Django 4.2.4 on 2023-11-04 04:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0008_rename_image_productimage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=50, null=True)),
                ('discount_amount', models.PositiveIntegerField()),
                ('start_date', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
    ]