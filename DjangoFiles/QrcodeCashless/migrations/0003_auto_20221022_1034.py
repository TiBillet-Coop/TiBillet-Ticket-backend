# Generated by Django 3.2 on 2022-10-22 06:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0002_alter_client_categorie'),
        ('QrcodeCashless', '0002_alter_detail_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Customers.client')),
            ],
        ),
        migrations.AlterField(
            model_name='cartecashless',
            name='number',
            field=models.CharField(db_index=True, editable=False, max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='cartecashless',
            name='tag_id',
            field=models.CharField(db_index=True, editable=False, max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='cartecashless',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True, verbose_name='Uuid'),
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('qty', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('last_date_used', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='QrcodeCashless.asset')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assets', to='QrcodeCashless.cartecashless')),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Portefeuilles',
                'unique_together': {('asset', 'card')},
            },
        ),
    ]
