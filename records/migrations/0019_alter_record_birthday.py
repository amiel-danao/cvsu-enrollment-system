# Generated by Django 4.1 on 2022-11-01 12:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0018_formsapproval_alter_record_birthday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2022, 11, 1, 20, 58, 52, 103203)),
        ),
    ]
