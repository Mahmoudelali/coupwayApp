# Generated by Django 4.2.4 on 2023-09-09 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preferences',
            name='prefered_subcategories_ids',
        ),
    ]