# Generated by Django 4.1 on 2022-10-31 01:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0015_alter_record_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2022, 10, 31, 9, 51, 16, 249398)),
        ),
    ]
