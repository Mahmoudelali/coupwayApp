# Generated by Django 4.2.4 on 2023-09-09 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0016_remove_category_parent_category_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='subcategories',
            field=models.ManyToManyField(to='offers.subcategory'),
        ),
    ]