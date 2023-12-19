# Generated by Django 4.2.4 on 2023-11-07 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0010_alter_offer_discount_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
