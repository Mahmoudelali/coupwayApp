# Generated by Django 4.2.3 on 2024-10-13 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0025_remove_offerdate_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='offer_dates',
        ),
        migrations.AddField(
            model_name='offerdate',
            name='offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='offers.offer'),
        ),
    ]
