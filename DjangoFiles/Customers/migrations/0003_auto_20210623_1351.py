# Generated by Django 2.2 on 2021-06-23 09:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0002_create_tenant_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='on_trial',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='paid_until',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
