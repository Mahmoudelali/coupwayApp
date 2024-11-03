# Generated by Django 4.2.4 on 2023-09-18 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0020_offer_days_of_week_offer_end_time_offer_months_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayOfWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='offer',
            name='days_of_week',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='months',
        ),
        migrations.AddField(
            model_name='offer',
            name='days_of_week',
            field=models.ManyToManyField(blank=True, to='offers.dayofweek'),
        ),
        migrations.AddField(
            model_name='offer',
            name='months',
            field=models.ManyToManyField(blank=True, to='offers.month'),
        ),
    ]