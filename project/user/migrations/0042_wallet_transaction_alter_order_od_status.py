# Generated by Django 4.2.4 on 2023-11-14 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0041_alter_order_od_status_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.transaction'),
        ),
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Return', 'Return'), ('Processing', 'Processing')], default='pending', max_length=150, null=True),
        ),
    ]
