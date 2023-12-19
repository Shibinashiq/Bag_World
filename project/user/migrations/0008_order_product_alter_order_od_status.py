# Generated by Django 4.2.6 on 2023-10-27 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0008_rename_image_productimage_image'),
        ('user', '0007_rename_profile_order_profile_alter_order_od_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_side.product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Return', 'Return'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='pending', max_length=150, null=True),
        ),
    ]
