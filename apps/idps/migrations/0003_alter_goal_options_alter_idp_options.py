# Generated by Django 5.0.1 on 2024-01-30 04:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("idps", "0002_alter_goal_deadline"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="goal",
            options={
                "ordering": (
                    "id",
                    "created_at",
                    "idp__title",
                    "status",
                    "deadline",
                ),
                "verbose_name": "Цель ИПР",
                "verbose_name_plural": "Цели для ИПР",
            },
        ),
        migrations.AlterModelOptions(
            name="idp",
            options={
                "ordering": (
                    "id",
                    "created_at",
                    "employee",
                    "chief",
                    "status",
                ),
                "verbose_name": "ИПР",
                "verbose_name_plural": "ИПРы",
            },
        ),
    ]
