# Generated by Django 4.2.6 on 2023-11-09 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginCodes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hash', models.CharField(max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
