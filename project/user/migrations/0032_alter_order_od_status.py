# Generated by Django 4.2.4 on 2023-11-08 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Processing', 'Processing'), ('Return', 'Return'), ('Cancelled', 'Cancelled')], default='pending', max_length=150, null=True),
        ),
    ]