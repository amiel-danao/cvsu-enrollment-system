# Generated by Django 4.1 on 2022-11-20 05:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_alter_record_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2022, 11, 20, 13, 27, 8, 314389)),
        ),
    ]
