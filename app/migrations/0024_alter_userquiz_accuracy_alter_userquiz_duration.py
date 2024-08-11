# Generated by Django 5.0.6 on 2024-08-11 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0023_alter_answer_duration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userquiz",
            name="accuracy",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=6, verbose_name="Точность"
            ),
        ),
        migrations.AlterField(
            model_name="userquiz",
            name="duration",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=6,
                verbose_name="Продолжительность",
            ),
        ),
    ]