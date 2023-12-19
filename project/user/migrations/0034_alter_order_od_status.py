# Generated by Django 4.2.4 on 2023-11-09 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0033_order_shipping_cost_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Processing', 'Processing'), ('Return', 'Return'), ('Shipped', 'Shipped'), ('Pending', 'Pending')], default='pending', max_length=150, null=True),
        ),
    ]
