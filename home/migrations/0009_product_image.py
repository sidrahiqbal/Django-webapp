# Generated by Django 4.1 on 2022-08-12 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='home/images'),
        ),
    ]
