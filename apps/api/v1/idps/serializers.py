from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.api.v1.users.serializers.users import (
    UserFIOSerializer,
    UserSerializer,
)
from apps.idps.models import Comment, GoalForIdp, Idp, Task
from apps.users.models import User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("text",)


class IdpForEmployeesSerializer(serializers.ModelSerializer):
    """Сериализация данных об ИПР.
    Используется в сериализаторе EmployeeSerializer.
    """

    class Meta:
        model = Idp
        fields = ["id", "title", "status"]


# class GoalTaskSerializer(serializers.ModelSerializer):
#     text = serializers.ReadOnlyField(source="tasks.text")
#
#     class Meta:
#         model = GoalForIdp
#         fields = ("text",)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментов, используется в
    сериализаторе IdpSerializer
    """

    user = UserFIOSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "comment_text", "created_at"]


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment_text",)
        read_only_fields = ("author", "user")


class GoalForIdpSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    comments = CommentSerializer(
        source="goal_comment", many=True, read_only=True
    )

    class Meta:
        model = GoalForIdp
        fields = (
            "id",
            "title",
            "deadline",
            "status",
            "description",
            "tasks",
            "comments",
        )


class PostGoalForIdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для целей у конкретного ИПР. POST запрос
    """

    tasks = TaskSerializer(many=True)

    class Meta:
        model = GoalForIdp
        fields = ("title", "description", "deadline", "tasks")


class PatchGoalForIdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для целей у конкретного ИПР. POST запрос
    """

    tasks = TaskSerializer(many=True)

    class Meta:
        model = GoalForIdp
        fields = ("id", "title", "description", "deadline", "tasks")
        read_only_fields = ("id",)


class IdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения ИПР. GET запрос
    """

    goals = GoalForIdpSerializer(source="idp_goals", many=True, read_only=True)

    employee = UserSerializer(read_only=True)

    # chief = UserSerializer(read_only=True)

    class Meta:
        model = Idp
        fields = ("id", "title", "status", "goals", "employee")  # "chief"


def create_goals_for_idp(goals, idp):
    """
    Функция создания целей для ИПР в БД
    """
    list_of_task = []
    for goal in goals:
        tasks = goal.pop("tasks")
        goal_obj = GoalForIdp.objects.create(**goal, idp=idp)
        for task in tasks:
            task_obj, created = Task.objects.get_or_create(task)
            list_of_task.append(task_obj.id)
        goal_obj.tasks.set(list_of_task)


class PostIdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания ИПР. POST запрос
    """

    goals = PostGoalForIdpSerializer(many=True)
    employee = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="id"
    )

    class Meta:
        model = Idp
        fields = ("title", "goals", "employee", "chief")
        read_only_fields = ("chief",)

    def create(self, validated_data):
        """
        Функция создания ИПР в БД
        """
        goals = validated_data.pop("goals")
        idp = Idp.objects.create(
            **validated_data, chief=self.context["request"].user
        )
        create_goals_for_idp(goals, idp)
        return idp

    def to_representation(self, instance):
        return IdpSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class PatchIdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения ИПР. PUT запрос
    """

    goals = PatchGoalForIdpSerializer(many=True)

    class Meta:
        model = Idp
        fields = (
            "id",
            "title",
            "goals",
            "status",
        )

    def update(self, instance, validated_data):
        """
        Функция для Put запроса
        """
        if instance.chief != self.context["request"].user:
            raise ValidationError("Исправлять может только автор")

        idp = get_object_or_404(Idp, id=instance.id)  # Старый ИПР
        goals = GoalForIdp.objects.filter(idp=idp.id)  # Старые цели

        new_goals = validated_data.pop("goals")  # новые цели
        super().update(instance, validated_data)  # обновили ИПР
        # new_tasks = new_goals.pop("tasks")  # новые таски
        for goal in goals:
            Task.objects.filter(goals=goal).delete()
        print(new_goals)
        # еще не закончила

        # return super().update(instance, validated_data)

    def to_representation(self, instance):
        return IdpSerializer(
            instance, context={"request": self.context.get("request")}
        ).data
