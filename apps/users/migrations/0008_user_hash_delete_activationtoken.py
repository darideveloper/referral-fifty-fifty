# Generated by Django 4.2.6 on 2023-11-06 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_activationlink_activationtoken_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hash',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.DeleteModel(
            name='ActivationToken',
        ),
    ]