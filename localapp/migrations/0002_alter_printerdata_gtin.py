# Generated by Django 5.0.6 on 2024-05-22 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printerdata',
            name='gtin',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
