# Generated by Django 5.0.6 on 2024-07-01 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_answer_created_at_alter_answer_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_recommendation',
            field=models.BooleanField(default=False, verbose_name='Есть ли рекомендация'),
        ),
        migrations.AddField(
            model_name='question',
            name='recommendation',
            field=models.TextField(blank=True, null=True, verbose_name='Рекомендация'),
        ),
    ]
