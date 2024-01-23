from rest_framework import serializers

from apps.api.v1.users.serializers.users import UserSerializer
from apps.idps.models import GoalForIdp, GoalTask, Idp


class IdpForEmployeesSerializer(serializers.ModelSerializer):
    """Сериализация данных об ИПР.
    Используется в сериализаторе EmployeeSerializer.
    """

    class Meta:
        model = Idp
        fields = ["id", "title", "status"]


class GoalTaskSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="tasks.id")
    text = serializers.ReadOnlyField(source="tasks.text")

    class Meta:
        model = GoalForIdp
        fields = ("id", "text")


class GoalForIdpSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="goal.id")
    title = serializers.ReadOnlyField(source="goal.title")
    description = serializers.ReadOnlyField(source="goal.description")
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        return GoalTaskSerializer(
            GoalTask.objects.filter(goal=obj.goal), many=True
        ).data

    class Meta:
        model = GoalForIdp
        fields = ("id", "title", "deadline", "status", "description", "tasks")


class IdpSerializer(serializers.ModelSerializer):
    goals = serializers.SerializerMethodField()
    employee = UserSerializer(read_only=True)
    chief = UserSerializer(read_only=True)

    def get_goals(self, obj):
        return GoalForIdpSerializer(
            GoalForIdp.objects.filter(idp=obj), many=True
        ).data

    class Meta:
        model = Idp
        fields = ("id", "title", "goals", "employee", "chief", "status")


# class PostIdpSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Idp
#         fields = (
#             "id", "title", "goals", "employee", "chief", "status"
#         )
