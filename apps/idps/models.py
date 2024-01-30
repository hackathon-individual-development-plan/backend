from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint

from apps.api.v1.validators import deadline_validator
from apps.users.models import ChiefEmployee, CommonCleanMixin, User


class Status(models.TextChoices):
    """Варианты статусов."""

    IN_PROGRESS = ("В работе", "In progress")
    WORK_DONE = ("Выполнен", "Work done")
    NOT_DONE = ("Не выполнен", "Not done")


class Idp(CommonCleanMixin, models.Model):
    """Модель ИПР (индивидуального плана развития)."""

    title = models.CharField(
        max_length=settings.FIELD_TITLE_LENGTH, verbose_name="Наименование ИПР"
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Сотрудник",
        related_name="my_idp",
    )
    chief = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Руководитель",
        related_name="idp_for_employee",
    )
    status = models.CharField(
        max_length=max([len(status) for status in Status]),
        choices=Status,
        default=Status.IN_PROGRESS,
        verbose_name="Статус ИПР",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, db_index=True
    )
    finished_at = models.DateTimeField(
        verbose_name="Дата закрытия ИПР", blank=True, null=True, db_index=True
    )

    class Meta:
        verbose_name = "ИПР"
        verbose_name_plural = "ИПРы"
        constraints = [
            UniqueConstraint(
                fields=["title", "chief", "employee"],
                name="Возможно это не ваш сотрудник?",
            ),
            UniqueConstraint(
                name="У сотрудника уже есть ИПР со статусом 'В работе'",
                fields=["employee"],
                condition=models.Q(status=Status.IN_PROGRESS),
            ),
            CheckConstraint(
                name="self_follow",
                check=~models.Q(chief=models.F("employee")),
            ),
        ]
        ordering = ("id", "created_at", "employee", "chief", "status")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if not ChiefEmployee.objects.filter(
            chief=self.chief, employee=self.employee
        ).exists():
            raise ValidationError("Возможно это не ваш сотрудник?")
        if self.status == Status.IN_PROGRESS:
            if Idp.objects.filter(
                employee=self.employee, status=Status.IN_PROGRESS
            ).exclude(pk=self.pk):
                raise ValidationError(
                    "У сотрудника уже есть ИПР со статусом 'В работе'"
                )


class Goal(models.Model):
    """Модель цели."""

    title = models.CharField(
        max_length=settings.FIELD_TITLE_LENGTH, verbose_name="Название Цели"
    )
    description = models.TextField(verbose_name="Описание Цели")
    status = models.CharField(
        max_length=max([len(status) for status in Status]),
        choices=Status,
        default=Status.IN_PROGRESS,
        verbose_name="Статус Цели",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, db_index=True
    )
    deadline = models.DateTimeField(
        verbose_name="Дата дедлайна",
        db_index=True,
        validators=(deadline_validator,),
    )
    idp = models.ForeignKey(
        Idp,
        on_delete=models.CASCADE,
        related_name="idp_goals",
        verbose_name="ИПР",
    )
    finished_at = models.DateTimeField(
        verbose_name="Дата закрытия цели", blank=True, null=True, db_index=True
    )

    class Meta:
        verbose_name = "Цель ИПР"
        verbose_name_plural = "Цели для ИПР"
        ordering = ("id", "created_at", "idp__title", "status", "deadline")

    def __str__(self):
        return self.title


class Task(models.Model):
    """Модель задачи."""

    text = models.TextField(verbose_name="Задача")
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="goals_tasks",
        verbose_name="Цели",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = (
            "text",
            "created_at",
        )

    def __str__(self):
        return f"id {self.id}-{self.text}"


class Comment(models.Model):
    """Модель комментария."""

    comment_text = models.TextField(verbose_name="Текст комментария")
    goal = models.ForeignKey(
        Goal,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="goal_comment",
        verbose_name="Цель",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_comments",
        verbose_name="Автор комментария",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий пользователя: {self.user.get_full_name()}"
