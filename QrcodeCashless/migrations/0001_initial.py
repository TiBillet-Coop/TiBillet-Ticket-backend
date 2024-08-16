# Generated by Django 3.2 on 2022-04-07 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stdimage.models
import stdimage.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', stdimage.models.StdImageField(blank=True, null=True, upload_to='images/', validators=[stdimage.validators.MaxSizeValidator(1920, 1920)], verbose_name='Recto de la carte')),
                ('img_url', models.URLField(blank=True, null=True)),
                ('base_url', models.CharField(blank=True, max_length=60, null=True)),
                ('generation', models.SmallIntegerField()),
                ('origine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origine', to='Customers.client')),
            ],
        ),
        migrations.CreateModel(
            name='CarteCashless',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.CharField(db_index=True, max_length=8, unique=True)),
                ('uuid', models.UUIDField(blank=True, null=True, verbose_name='Uuid')),
                ('number', models.CharField(db_index=True, max_length=8, unique=True)),
                ('detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QrcodeCashless.detail')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]