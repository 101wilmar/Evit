# Generated by Django 5.0.6 on 2024-06-19 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_useranswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquiz',
            name='height',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='userquiz',
            name='weight',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]