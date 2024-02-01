# Generated by Django 4.2.6 on 2024-01-31 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0074_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Return', 'Return'), ('Processing', 'Processing'), ('Delivered', 'Delivered'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped')], default='pending', max_length=150, null=True),
        ),
    ]