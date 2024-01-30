# Generated by Django 5.0.1 on 2024-01-30 16:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("idps", "0004_remove_idp_unique_idp_for_employee_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="goal",
            name="status",
            field=models.CharField(
                choices=[
                    ("В работе", "In progress"),
                    ("Выполнен", "Work done"),
                    ("Не выполнен", "Not done"),
                ],
                default="В работе",
                max_length=11,
                verbose_name="Статус Цели",
            ),
        ),
        migrations.AlterField(
            model_name="idp",
            name="status",
            field=models.CharField(
                choices=[
                    ("В работе", "In progress"),
                    ("Выполнен", "Work done"),
                    ("Не выполнен", "Not done"),
                ],
                default="В работе",
                max_length=11,
                verbose_name="Статус ИПР",
            ),
        ),
        migrations.AddConstraint(
            model_name="idp",
            constraint=models.UniqueConstraint(
                condition=models.Q(("status", "В работе")),
                fields=("employee",),
                name="У сотрудника уже есть ИПР со статусом 'В работе'",
            ),
        ),
    ]
