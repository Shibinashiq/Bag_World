# Generated by Django 4.2.6 on 2023-10-13 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
                ('brand_image', models.ImageField(upload_to='brands_image/')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_image', models.ImageField(upload_to='cat_photos')),
                ('category_name', models.CharField(max_length=25)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(null=True, upload_to='product_image/')),
                ('product_name', models.CharField(max_length=255, null=True)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('product_offer', models.CharField(max_length=25, null=True)),
                ('product_quantity', models.PositiveIntegerField(null=True)),
                ('product_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_side.brand')),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_side.category')),
            ],
        ),
    ]
