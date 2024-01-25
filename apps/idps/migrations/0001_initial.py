# Generated by Django 5.0.1 on 2024-01-25 16:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GoalForIdp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=200, verbose_name="Название Цели"
                    ),
                ),
                (
                    "description",
                    models.TextField(verbose_name="Описание Цели"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("In progress", "В работе"),
                            ("Work done", "Выполнен"),
                            ("Not done", "Не выполнен"),
                            ("Empty", "Отсутствует"),
                        ],
                        default="In progress",
                        max_length=11,
                        verbose_name="Статус Цели",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "deadline",
                    models.DateTimeField(
                        db_index=True, verbose_name="Дата дедлайна"
                    ),
                ),
                (
                    "finished_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Дата закрытия цели",
                    ),
                ),
            ],
            options={
                "verbose_name": "Цель ИПР",
                "verbose_name_plural": "Цели для ИПР",
                "ordering": ("created_at", "idp__title", "status", "deadline"),
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "comment_text",
                    models.TextField(verbose_name="Текст комментария"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_comments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор комментария",
                    ),
                ),
                (
                    "goal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goal_comment",
                        to="idps.goalforidp",
                        verbose_name="Цель",
                    ),
                ),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.CreateModel(
            name="Idp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=200, verbose_name="Наименование ИПР"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("In progress", "В работе"),
                            ("Work done", "Выполнен"),
                            ("Not done", "Не выполнен"),
                            ("Empty", "Отсутствует"),
                        ],
                        default="In progress",
                        max_length=11,
                        verbose_name="Статус ИПР",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "finished_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="Дата закрытия ИПР",
                    ),
                ),
                (
                    "chief",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="idp_for_employee",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Руководитель",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="my_idp",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Сотрудник",
                    ),
                ),
            ],
            options={
                "verbose_name": "ИПР",
                "verbose_name_plural": "ИПРы",
                "ordering": ("created_at", "employee", "chief", "status"),
            },
        ),
        migrations.AddField(
            model_name="goalforidp",
            name="idp",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="idp_goals",
                to="idps.idp",
                verbose_name="ИПР",
            ),
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="Задача")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "goal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goals_tasks",
                        to="idps.goalforidp",
                        verbose_name="Цели",
                    ),
                ),
            ],
            options={
                "verbose_name": "Задача",
                "verbose_name_plural": "Задачи",
                "ordering": ("text", "created_at"),
            },
        ),
        migrations.AddConstraint(
            model_name="idp",
            constraint=models.UniqueConstraint(
                fields=("title", "chief", "employee"),
                name="unique_idp_for_employee",
            ),
        ),
        migrations.AddConstraint(
            model_name="idp",
            constraint=models.CheckConstraint(
                check=models.Q(("chief", models.F("employee")), _negated=True),
                name="self_follow",
            ),
        ),
    ]
