# Generated by Django 4.2.4 on 2023-08-31 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0009_alter_feedbacks_feedback_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='feedbacks',
        ),
    ]