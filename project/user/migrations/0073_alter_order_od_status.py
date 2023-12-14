# Generated by Django 4.2.6 on 2023-12-14 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0072_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Processing', 'Processing'), ('Return', 'Return')], default='pending', max_length=150, null=True),
        ),
    ]