# Generated by Django 4.2.4 on 2023-08-28 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_rename_name_location_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='title',
            new_name='name',
        ),
    ]
