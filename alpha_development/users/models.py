from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class CommonCleanMixin(models.Model):
    """
    Выполняет общие проверки для моделей, наследующих CommonCleanMixin.
    Используется в моделях ChiefEmployee и Idp.
    """

    class Meta:
        abstract = True

    def clean(self):
        if self.chief_id is None or self.employee_id is None:
            raise ValidationError(
                {
                    "chief": ["Необходимо выбрать руководителя."],
                    "employee": ["Необходимо выбрать сотрудника."],
                }
            )
        if self.chief == self.employee:
            raise ValidationError("Вы не можете назначать самого себя!")
        if not UserRole.objects.filter(
            user=self.chief, role=Role.CHIEF
        ).exists():
            raise ValidationError(
                "Руководитель должен иметь соответствующую роль!"
            )
        if not UserRole.objects.filter(
            user=self.employee, role=Role.EMPLOYEE
        ).exists():
            raise ValidationError(
                "Сотрудник должен иметь соответствующую роль!"
            )


class Role(models.TextChoices):
    """Варианты ролей пользователя."""

    CHIEF = ("chief", "Руководитель")
    EMPLOYEE = ("employee", "Сотрудник")


class User(AbstractUser):
    """Модель пользователя."""

    fio = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="ФИО"
    )
    job_title = models.CharField(
        max_length=150, blank=False, null=False, verbose_name="Должность"
    )
    photo = models.ImageField(
        upload_to="user_photos/", blank=True, null=True, verbose_name="Фото"
    )

    class Meta:
        swappable = "AUTH_USER_MODEL"
        ordering = ("fio",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class UserRole(models.Model):
    """
    Модель для связи между пользователями и их ролями.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Пользователь",
    )
    role = models.CharField(
        max_length=10,
        choices=Role,
        default=Role.EMPLOYEE,
        verbose_name="Роль",
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "role"], name="unique_user_role")
        ]
        verbose_name = "Роль пользователя"
        verbose_name_plural = "Роли пользователей"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class ChiefEmployee(CommonCleanMixin, models.Model):
    """
    Модель для связи между руководителями и их сотрудниками.
    """

    chief = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chief",
        verbose_name="Руководитель",
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="employee",
        verbose_name="Сотрудник",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["employee", "chief"], name="unique_employee_chief"
            )
        ]
        verbose_name = "Сотрудник и руководитель"
        verbose_name_plural = "Сотрудники и руководители"

    def __str__(self):
        return f"{self.chief.username} - {self.employee.username}"

    def clean(self):
        super().clean()
        chiefs_count = ChiefEmployee.objects.filter(
            employee=self.employee
        ).count()
        if chiefs_count > 0:
            raise ValidationError("У сотрудника уже есть руководитель!")
