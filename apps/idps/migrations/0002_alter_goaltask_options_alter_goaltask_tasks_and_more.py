# Generated by Django 5.0.1 on 2024-01-20 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("idps", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="goaltask",
            options={
                "verbose_name": "Цель-задача",
                "verbose_name_plural": "Цели - задачи",
            },
        ),
        migrations.AlterField(
            model_name="goaltask",
            name="tasks",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="goals",
                to="idps.task",
                verbose_name="Цель",
            ),
        ),
        migrations.AddConstraint(
            model_name="goaltask",
            constraint=models.UniqueConstraint(
                fields=("goal", "tasks"), name="unique_goal_task"
            ),
        ),
    ]
