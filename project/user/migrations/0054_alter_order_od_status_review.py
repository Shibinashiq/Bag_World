# Generated by Django 4.2.6 on 2023-11-17 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0020_alter_coupon_coupon_code_alter_offer_discount_amount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0053_alter_order_od_status_delete_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='od_status',
            field=models.CharField(choices=[('Return', 'Return'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Processing', 'Processing'), ('Pending', 'Pending'), ('Shipped', 'Shipped')], default='pending', max_length=150, null=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_side.product')),
                ('user_instance', models.ForeignKey(blank=True, default=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
