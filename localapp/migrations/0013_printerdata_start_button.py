# Generated by Django 5.0.6 on 2024-06-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localapp', '0012_remove_printerdata_jobstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='printerdata',
            name='start_button',
            field=models.BooleanField(default=False),
        ),
    ]
