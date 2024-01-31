import datetime

from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.api.v1.users.serializers.users import (
    UserFIOSerializer,
    UserSerializer,
)
from apps.api.v1.validators import deadline_validator, idp_validator
from apps.idps.models import Comment, Goal, Idp, Status, Task
from apps.users.models import User


class IdpForEmployeesSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра данных об ИПР.
    Используется в сериализаторе EmployeeSerializer.
    """

    class Meta:
        model = Idp
        fields = ["id", "title", "status"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра комментариев.
    Используется в сериализаторе IdpSerializer.
    """

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    user = UserFIOSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "comment_text", "created_at"]


class PostCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания комментариев."""

    class Meta:
        model = Comment
        fields = ("comment_text",)
        read_only_fields = ("author", "user")


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и редактирования задач.
    id - опционально.
    """

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = (
            "id",
            "text",
        )


class PostTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для создания задач."""

    class Meta:
        model = Task
        fields = ("text",)


class GoalSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных о целях ИПР."""

    deadline = serializers.DateTimeField(format="%Y-%m-%d")
    tasks = TaskSerializer(source="goals_tasks", many=True, read_only=True)
    comments = CommentSerializer(
        source="goal_comment", many=True, read_only=True
    )

    class Meta:
        model = Goal
        fields = (
            "id",
            "title",
            "deadline",
            "status",
            "description",
            "tasks",
            "comments",
        )


class PostGoalSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания целей ИПР.
    """

    deadline = serializers.DateTimeField(validators=[deadline_validator])
    tasks = PostTaskSerializer(many=True)

    class Meta:
        model = Goal
        fields = ("title", "description", "deadline", "tasks")


class PutGoalSerializer(serializers.ModelSerializer):
    """
    Сериализатор для редактирования целей ИПР.
    id - опционально.
    """

    deadline = serializers.DateTimeField(validators=[deadline_validator])
    id = serializers.IntegerField(required=False)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Goal
        fields = ("id", "title", "description", "deadline", "status", "tasks")


class IdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра ИПР руководителем.
    """

    goals = GoalSerializer(source="idp_goals", many=True, read_only=True)
    employee = UserSerializer(read_only=True)

    class Meta:
        model = Idp
        fields = ("id", "title", "status", "goals", "employee")


class MyIdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра ИПР сотрудником.
    """

    goals = GoalSerializer(source="idp_goals", many=True, read_only=True)

    class Meta:
        model = Idp
        fields = ("id", "title", "status", "goals")


class PostIdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания ИПР.
    """

    goals = PostGoalSerializer(many=True)
    employee = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="id",
        validators=[
            UniqueValidator(
                queryset=Idp.objects.filter(status=Status.IN_PROGRESS),
                message="У сотрудника уже есть ИПР со статусом 'В работе'!",
            )
        ],
    )

    class Meta:
        model = Idp
        fields = ("title", "goals", "employee", "chief")
        read_only_fields = ("chief",)

    def create_goals_for_idp(self, goals, idp):
        with transaction.atomic():
            for goal in goals:
                tasks = goal.pop("tasks")
                goal_obj = Goal.objects.create(**goal, idp=idp)
                tasks_to_create = [
                    Task(**task, goal_id=goal_obj.id) for task in tasks
                ]
                Task.objects.bulk_create(tasks_to_create)

    def create(self, validated_data):
        goals = validated_data.pop("goals")
        with transaction.atomic():
            idp = Idp.objects.create(
                **validated_data, chief=self.context["request"].user
            )
            self.create_goals_for_idp(goals, idp)
        return idp

    def validate(self, data):
        return idp_validator(self, data, Idp)

    def to_representation(self, instance):
        return IdpSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class PutIdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для редактирования ИПР.
    """

    goals = PutGoalSerializer(many=True)

    class Meta:
        model = Idp
        fields = (
            "id",
            "title",
            "goals",
            "status",
        )

    def update(self, instance, validated_data):
        if instance.chief != self.context["request"].user:
            raise ValidationError("Исправлять может только автор")

        with transaction.atomic():
            goals_data = validated_data.pop("goals")
            goals_ids = [
                goal_data.get("id", None)
                for goal_data in goals_data
                if goal_data.get("id", None) is not None
            ]
            # Удаление целей, которых нет в запросе
            instance.idp_goals.exclude(id__in=goals_ids).delete()
            # Проставление даты закрытия ИПР
            if validated_data["status"] == Status.WORK_DONE:
                validated_data["finished_at"] = datetime.datetime.now()
            super().update(instance, validated_data)
            # Обновление существующих целей или создание новых целей
            for goal_data in goals_data:
                goal_id = goal_data.get("id", None)
                tasks_data = goal_data.pop("tasks", [])
                if goal_id is not None:
                    # Обновление существующей цели
                    if goal_data["status"] == Status.WORK_DONE:
                        goal_data["finished_at"] = datetime.datetime.now()
                    goal_instance = get_object_or_404(Goal, id=goal_id)
                    super().update(goal_instance, goal_data)

                    # Обновление задач для цели
                    self.update_or_create_tasks(goal_instance, tasks_data)

                else:
                    # Создание новой цели
                    goal_serializer = GoalSerializer(data=goal_data)
                    goal_serializer.is_valid(raise_exception=True)
                    goal_instance = goal_serializer.save(idp=instance)

                    # Создание задач для новой цели
                    self.update_or_create_tasks(goal_instance, tasks_data)
        return instance

    def update_or_create_tasks(self, goal_instance, tasks_data):
        tasks_ids = [
            task_data.get("id", None)
            for task_data in tasks_data
            if task_data.get("id", None) is not None
        ]

        # Удаление задач, которых нет в запросе
        goal_instance.goals_tasks.exclude(id__in=tasks_ids).delete()

        for task_data in tasks_data:
            task_id = task_data.get("id", None)

            if task_id is not None:
                # Обновление существующей задачи
                task_instance = get_object_or_404(Task, id=task_id)
                super().update(task_instance, task_data)
            else:
                # Создание новой задачи
                task_serializer = TaskSerializer(data=task_data)
                task_serializer.is_valid(raise_exception=True)
                task_serializer.save(goal=goal_instance)

    def validate(self, data):
        return idp_validator(self, data, Idp)

    def to_representation(self, instance):
        return IdpSerializer(
            instance, context={"request": self.context.get("request")}
        ).data
