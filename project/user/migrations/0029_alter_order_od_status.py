# Generated by Django 4.2.4 on 2023-11-07 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Return', 'Return'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Processing', 'Processing')], default='pending', max_length=150, null=True),
        ),
    ]
