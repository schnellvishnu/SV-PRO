# Generated by Django 3.2.5 on 2024-07-08 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverdataapp', '0004_serverprinterdata_load_button_resp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverprinterdata',
            name='serverstatus',
            field=models.CharField(default='Not Updated', max_length=100),
        ),
    ]
