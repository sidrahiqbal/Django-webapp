# Generated by Django 4.1 on 2022-09-15 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_order_status_alter_order_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='thumbnails_urls',
        ),
        migrations.AddField(
            model_name='product',
            name='care',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='product',
            name='image_urls',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.TextField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('Donna', 'Donna'), ('Uomo', 'Uomo')], max_length=10),
        ),
    ]
