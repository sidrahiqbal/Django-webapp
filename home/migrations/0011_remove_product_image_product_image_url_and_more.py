# Generated by Django 4.1 on 2022-08-16 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_product_image_url_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], max_length=10),
        ),
    ]
