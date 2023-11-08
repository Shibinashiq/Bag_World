# Generated by Django 4.2.4 on 2023-11-07 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Return', 'Return'), ('Delivered', 'Delivered')], default='pending', max_length=150, null=True),
        ),
    ]