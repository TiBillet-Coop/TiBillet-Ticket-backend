# Generated by Django 4.2.17 on 2025-01-07 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0116_membership_uuid_alter_configuration_federated_with_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='externalapikey',
            name='revoquer_apikey',
        ),
        migrations.AlterField(
            model_name='externalapikey',
            name='reservation',
            field=models.BooleanField(default=False, verbose_name='Créer des reservations'),
        ),
        migrations.AlterField(
            model_name='webhook',
            name='event',
            field=models.CharField(choices=[('MV', 'Adhésion validée'), ('RV', 'Réservation validée')], default='RV', max_length=2, verbose_name='Évènement'),
        ),
    ]
