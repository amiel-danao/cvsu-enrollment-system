# Generated by Django 4.1 on 2023-01-18 02:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_alter_record_school_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='registration_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
