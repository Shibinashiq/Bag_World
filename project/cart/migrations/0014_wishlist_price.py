# Generated by Django 4.2.4 on 2023-11-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_remove_wishlist_offer_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
