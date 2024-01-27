import datetime
import datetime as dt

from rest_framework.exceptions import ValidationError


def deadline_validator(value):
    if value < dt.datetime.now(datetime.timezone.utc) + dt.timedelta(days=1):
        raise ValidationError(
            "Дата дедлайна должна быть больше, чем сейчас хотя бы на один "
            "день"
        )
