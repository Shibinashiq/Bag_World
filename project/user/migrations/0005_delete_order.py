# Generated by Django 4.2.6 on 2023-10-25 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_order_od_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]