from rest_framework import serializers

from apps.idps.models import Idp


class IdpForEmployeesSerializer(serializers.ModelSerializer):
    """Сериализация данных об ИПР.

    Используется в сериализаторе EmployeeSerializer.
    """

    class Meta:
        model = Idp
        fields = ["id", "title", "status"]
