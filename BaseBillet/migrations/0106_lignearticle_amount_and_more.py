# Generated by Django 4.2.17 on 2024-12-18 10:42

from django.db import migrations, models


class Migration(migrations.Migration):
    # atomic = False

    dependencies = [
        ('BaseBillet', '0105_lignearticle_payment_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignearticle',
            name='amount',
            field=models.SmallIntegerField(default=0, verbose_name='Montant'),
        ),
        migrations.AlterField(
            model_name='lignearticle',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('CB', 'Carte bancaire : TPE'), ('CS', 'Espèce'), ('CH', 'Cheque bancaire'), ('ST', 'En ligne : Stripe'), ('SR', 'Paiement récurent : Stripe')], max_length=2, null=True, verbose_name='Moyen de paiement'),
        ),
    ]