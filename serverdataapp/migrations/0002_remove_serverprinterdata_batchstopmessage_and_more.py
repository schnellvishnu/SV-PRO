# Generated by Django 5.0.6 on 2024-07-05 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serverdataapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serverprinterdata',
            name='batchstopmessage',
        ),
        migrations.RemoveField(
            model_name='serverprinterdata',
            name='label_response',
        ),
        migrations.RemoveField(
            model_name='serverprinterdata',
            name='loadpause',
        ),
        migrations.RemoveField(
            model_name='serverprinterdata',
            name='pause_stop_btnresponse',
        ),
        migrations.RemoveField(
            model_name='serverprinterdata',
            name='preparebuttonresponse',
        ),
        migrations.RemoveField(
            model_name='serverprinterdata',
            name='responsefield',
        ),
        migrations.RemoveField(
            model_name='serverprinterdata',
            name='return_slno_btn_response',
        ),
        migrations.RemoveField(
            model_name='serverprinterdata',
            name='start_pause_btnresponse',
        ),
        migrations.RemoveField(
            model_name='serverprinterdata',
            name='stopbtnresponse',
        ),
    ]
