# Generated by Django 3.2 on 2023-04-03 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0058_alter_paiement_stripe_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cashless',
            field=models.BooleanField(default=False, verbose_name='Proposer la recharge cashless'),
        ),
    ]
