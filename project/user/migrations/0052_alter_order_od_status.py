# Generated by Django 4.2.6 on 2023-11-17 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0051_alter_order_od_status_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Return', 'Return'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Delivered', 'Delivered')], default='pending', max_length=150, null=True),
        ),
    ]
