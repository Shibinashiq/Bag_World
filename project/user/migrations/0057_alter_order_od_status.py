# Generated by Django 4.2.4 on 2023-11-21 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0056_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Return', 'Return'), ('Processing', 'Processing'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Pending', 'Pending')], default='pending', max_length=150, null=True),
        ),
    ]
