# Generated by Django 5.0.6 on 2024-05-29 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localapp', '0003_printerdata_printerstatefield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printerdata',
            name='printerstatefield',
        ),
    ]
