# Generated by Django 4.2.17 on 2024-12-20 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0110_alter_lignearticle_payment_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='ligne_article',
            field=models.ManyToManyField(blank=True, related_name='membership', to='BaseBillet.lignearticle'),
        ),
    ]
