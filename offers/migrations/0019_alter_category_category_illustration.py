# Generated by Django 4.2.4 on 2023-09-14 23:26

from django.db import migrations, models
import offers.models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0018_category_category_illustration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_illustration',
            field=models.ImageField(blank=True, null=True, upload_to=offers.models.categories_image_upload_path),
        ),
    ]
