# Generated by Django 5.0.6 on 2024-07-04 17:34

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='recommendation',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Рекомендация'),
        ),
    ]
