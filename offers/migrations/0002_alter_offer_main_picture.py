# Generated by Django 4.2.4 on 2023-08-28 15:00

from django.db import migrations, models
import offers.models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='main_picture',
            field=models.ImageField(upload_to=offers.models.offer_image_upload_path),
        ),
    ]