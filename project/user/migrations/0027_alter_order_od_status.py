# Generated by Django 4.2.4 on 2023-11-07 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Return', 'Return'), ('Pending', 'Pending'), ('Delivered', 'Delivered')], default='pending', max_length=150, null=True),
        ),
    ]
