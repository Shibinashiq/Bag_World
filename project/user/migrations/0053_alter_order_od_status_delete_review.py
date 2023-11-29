# Generated by Django 4.2.6 on 2023-11-17 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0052_alter_order_od_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Processing', 'Processing'), ('Return', 'Return'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped')], default='pending', max_length=150, null=True),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]