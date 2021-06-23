# Generated by Django 2.2 on 2021-06-22 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0008_event_reservations'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionGenerale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='reservations',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='configuration',
            name='option_generale_checkbox',
            field=models.ManyToManyField(blank=True, related_name='checkbox', to='BaseBillet.OptionGenerale'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='option_generale_radio',
            field=models.ManyToManyField(blank=True, related_name='radiobutton', to='BaseBillet.OptionGenerale'),
        ),
    ]
