# Generated by Django 4.2.6 on 2023-12-13 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0067_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Return', 'Return'), ('Processing', 'Processing'), ('Delivered', 'Delivered')], default='pending', max_length=150, null=True),
        ),
    ]
