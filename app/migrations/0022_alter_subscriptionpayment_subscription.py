# Generated by Django 5.0.6 on 2024-07-05 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_rename_yokassa_id_subscriptionpayment_yookassa_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionpayment',
            name='subscription',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='app.subscription'),
        ),
    ]