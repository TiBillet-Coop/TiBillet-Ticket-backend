# Generated by Django 3.2 on 2022-01-22 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0033_rename_pricessold_pricesold'),
    ]

    operations = [
        migrations.AddField(
            model_name='paiement_stripe',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
