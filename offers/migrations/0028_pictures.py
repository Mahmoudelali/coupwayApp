# Generated by Django 4.2.3 on 2024-11-03 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0027_delete_pictures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inner_pic', models.ImageField(upload_to='offers/<django.db.models.fields.related.ForeignKey>/')),
                ('parent_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offers.offer')),
            ],
        ),
    ]