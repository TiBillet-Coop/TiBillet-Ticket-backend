# Generated by Django 3.2 on 2022-04-22 13:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AuthBillet', '0007_alter_terminalpairingtoken_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminalpairingtoken',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]