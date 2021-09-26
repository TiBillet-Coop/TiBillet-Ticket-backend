# Generated by Django 2.2 on 2021-09-23 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0026_auto_20210923_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lignearticle',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BaseBillet.Reservation'),
        ),
    ]