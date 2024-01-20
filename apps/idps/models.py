from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint


class Task(models.Model):
    """Модель задачи"""

    text = models.TextField(verbose_name="Задача")
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ("created_at",)

    def __str__(self):
        return self.text


class Goal(models.Model):
    """Модель цели"""

    title = models.CharField(
        max_length=settings.FIELD_TITLE_LENGTH, verbose_name="Название Цели"
    )
    description = models.TextField(verbose_name="Описание Цели")
    tasks = models.ManyToManyField(
        Task,
        blank=False,
        through="GoalTask",
        verbose_name="Задачи",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"
        ordering = ("created_at",)

    def __str__(self):
        return self.title


class GoalTask(models.Model):
    """Модель для связи целей с задачами"""

    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, null=False, verbose_name="Цель"
    )
    tasks = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=False,
        related_name="goals",
        verbose_name="Цель",
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["goal", "tasks"], name="unique_goal_task")
        ]
        verbose_name = "Цель-задача"
        verbose_name_plural = "Цели - задачи"

    def __str__(self):
        return f"Цель {self.goal.title} включает задачу {self.tasks.text}"
