# Generated by Django 4.1 on 2022-11-19 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='...'),
        ),
    ]
