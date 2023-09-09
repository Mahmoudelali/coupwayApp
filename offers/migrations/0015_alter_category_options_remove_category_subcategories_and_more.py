# Generated by Django 4.2.4 on 2023-09-09 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_remove_preferences_prefered_subcategories_ids'),
        ('offers', '0014_remove_subcategory_parent_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.RemoveField(
            model_name='category',
            name='Subcategories',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='sub',
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='offers.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.RemoveField(
            model_name='offer',
            name='category',
        ),
        migrations.DeleteModel(
            name='Subcategory',
        ),
        migrations.AddField(
            model_name='offer',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='offers.category'),
        ),
    ]
