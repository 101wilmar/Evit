# Generated by Django 5.0.6 on 2024-07-04 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_question_is_editable'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Payment',
            new_name='SubscriptionPayment',
        ),
    ]
