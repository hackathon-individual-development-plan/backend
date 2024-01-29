from rest_framework import serializers

from apps.users.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    """Сериализация данных, включая роль, о текущем сотруднике."""

    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "fio", "job_title", "photo", "role"]

    def get_role(self, obj):
        user_role = obj.user_role.first()
        return user_role.role if user_role else None


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотруднике: ФИО, должность и фото.

    Используется в сериализаторе EmployeeSerializer.
    """

    class Meta:
        model = User
        fields = ["id", "fio", "job_title", "photo"]


class UserFIOSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотруднике: ФИО.

    Используется в сериализаторе EmployeeWithoutIdpSerializer.
    """

    class Meta:
        model = User
        fields = ["id", "fio"]
