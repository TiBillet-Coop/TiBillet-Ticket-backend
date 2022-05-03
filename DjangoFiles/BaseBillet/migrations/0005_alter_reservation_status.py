# Generated by Django 3.2 on 2022-04-22 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0004_auto_20220421_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('C', 'Annulée'), ('R', 'Crée'), ('U', 'Non payée'), ('F', 'Mail non vérifié'), ('FA', 'Mail user vérifié'), ('P', 'Payée'), ('PE', 'Payée mais mail non valide'), ('PN', 'Payée mais mail non envoyé'), ('V', 'Validée')], default='R', max_length=3, verbose_name='Status de la réservation'),
        ),
    ]