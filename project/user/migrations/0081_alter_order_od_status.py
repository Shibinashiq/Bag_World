# Generated by Django 5.0.1 on 2024-02-02 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0080_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Processing', 'Processing'), ('Cancelled', 'Cancelled'), ('Return', 'Return'), ('Shipped', 'Shipped')], default='pending', max_length=150, null=True),
        ),
    ]
