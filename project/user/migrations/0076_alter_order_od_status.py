# Generated by Django 4.2.6 on 2024-02-01 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0075_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Processing', 'Processing'), ('Return', 'Return'), ('Delivered', 'Delivered')], default='pending', max_length=150, null=True),
        ),
    ]
