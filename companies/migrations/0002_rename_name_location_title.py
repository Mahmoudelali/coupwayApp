# Generated by Django 4.2.4 on 2023-08-28 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='name',
            new_name='title',
        ),
    ]
