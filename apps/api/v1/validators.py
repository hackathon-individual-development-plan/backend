import datetime
import datetime as dt

from rest_framework.exceptions import ValidationError


def deadline_validator(value):
    if value < dt.datetime.now(datetime.timezone.utc) + dt.timedelta(days=1):
        raise ValidationError(
            "Дата дедлайна должна быть больше, чем сейчас хотя бы на один "
            "день"
        )


def idp_validator(self, data, idp_model):
    errors = []
    goals = data.get("goals")
    if not goals:
        errors.append("Должна быть как минимум одна цель")
    for goal in goals:
        tasks = goal.get("tasks")
        if not tasks:
            errors.append("Должна быть как минимум одна задача")
    if self.context["request"].user == data.get("employee"):
        errors.append("Создать ИПР себе нельзя!")
    if idp_model.objects.filter(
        chief=self.context["request"].user,
        employee=data.get("employee"),
        title=data.get("title"),
    ):
        errors.append("У этого сотрудника уже есть ИПР с таким названием")
    if errors:
        raise ValidationError(errors)
    return data
