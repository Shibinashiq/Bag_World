# Generated by Django 4.2.6 on 2023-12-13 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0066_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Return', 'Return'), ('Processing', 'Processing'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped')], default='pending', max_length=150, null=True),
        ),
    ]
