# Generated by Django 4.2.11 on 2024-05-11 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0088_fedowtransaction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='vat',
            field=models.CharField(choices=[('NA', 'Non applicable'), ('DX', '10 %'), ('VG', '20 %'), ('HC', '8.5 %'), ('DD', '2.2 %')], default='NA', max_length=2, verbose_name='Taux TVA'),
        ),
    ]
