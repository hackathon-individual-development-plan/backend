from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотруднике: ФИО, должность и фото.

    Используется в сериализаторе EmployeeSerializer.
    """

    class Meta:
        model = User
        fields = ["fio", "job_title", "photo"]


class UserFIOSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотруднике: ФИО.

    Используется в сериализаторе EmployeeWithoutIdpSerializer.
    """

    class Meta:
        model = User
        fields = ["fio"]
