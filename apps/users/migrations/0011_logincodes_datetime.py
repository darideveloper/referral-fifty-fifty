# Generated by Django 4.2.6 on 2023-11-10 20:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_logincodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='logincodes',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
