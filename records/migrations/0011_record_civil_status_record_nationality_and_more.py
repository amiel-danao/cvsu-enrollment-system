# Generated by Django 4.1 on 2022-10-20 13:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0010_record_registration_status_alter_record_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='civil_status',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='record',
            name='nationality',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='record',
            name='religion',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='record',
            name='school_elementary',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='record',
            name='sex',
            field=models.PositiveIntegerField(choices=[(1, 'Male'), (2, 'Female')], default=1, max_length=1),
        ),
        migrations.AlterField(
            model_name='record',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2022, 10, 20, 21, 52, 48, 786080)),
        ),
    ]
