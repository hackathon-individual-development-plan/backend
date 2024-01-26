from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.api.v1.users.serializers.users import (
    UserFIOSerializer,
    UserSerializer,
)
from apps.idps.models import Comment, Goal, Idp, Task
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

    tasks = PostTaskSerializer(many=True)

    class Meta:
        model = Goal
        fields = ("title", "description", "deadline", "tasks")


class PutGoalSerializer(serializers.ModelSerializer):
    """
    Сериализатор для редактирования целей ИПР.
    id - опционально.
    """

    id = serializers.IntegerField(required=False)
    tasks = TaskSerializer(source="goals_tasks", many=True)

    class Meta:
        model = Goal
        fields = ("id", "title", "description", "deadline", "tasks")


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
        queryset=User.objects.all(), slug_field="id"
    )

    class Meta:
        model = Idp
        fields = ("title", "goals", "employee", "chief")
        read_only_fields = ("chief",)

    def create_goals_for_idp(self, goals, idp):
        list_of_task = []
        for goal in goals:
            tasks = goal.pop("tasks")
            goal_obj = Goal.objects.create(**goal, idp=idp)
            for task in tasks:
                task["goal_id"] = goal_obj.id
                task_obj, created = Task.objects.get_or_create(task)
                list_of_task.append(task_obj.id)

    def create(self, validated_data):
        goals = validated_data.pop("goals")
        idp = Idp.objects.create(
            **validated_data, chief=self.context["request"].user
        )
        self.create_goals_for_idp(goals, idp)
        return idp

    def to_representation(self, instance):
        return IdpSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class PutIdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для редактирования ИПР.
    """

    goals = PutGoalSerializer(source="idp_goals", many=True)

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

        goals_data = validated_data["idp_goals"]
        goals_ids = [
            goal_data.get("id", None)
            for goal_data in goals_data
            if goal_data.get("id", None) is not None
        ]
        # Удаление целей, которых нет в запросе
        instance.idp_goals.exclude(id__in=goals_ids).delete()

        # Обновление существующих целей или создание новых целей
        for goal_data in goals_data:
            goal_id = goal_data.get("id", None)
            tasks_data = goal_data.pop("goals_tasks", [])

            if goal_id is not None:
                # Обновление существующей цели
                goal_instance = get_object_or_404(
                    Goal, id=goal_id, idp=instance
                )
                goal_serializer = GoalSerializer(
                    goal_instance, data=goal_data, partial=True
                )
                goal_serializer.is_valid(raise_exception=True)
                goal_serializer.save()

                # Обновление задач для цели
                self.update_or_create_tasks(goal_instance, tasks_data)

            else:
                # Создание новой цели
                goal_serializer = GoalSerializer(data=goal_data)
                goal_serializer.is_valid(raise_exception=True)
                goal_instance = goal_serializer.save(idp=instance)

                # Создание задач для новой цели
                def drop(dictionary, dictionary_key):
                    dictionary.pop(dictionary_key)
                    return dictionary

                tasks_data = [drop(task, "id") for task in tasks_data]
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
                task_instance = get_object_or_404(
                    Task, id=task_id, goal=goal_instance
                )
                task_serializer = TaskSerializer(
                    task_instance, data=task_data, partial=True
                )
                task_serializer.is_valid(raise_exception=True)
                task_serializer.save()

            else:
                # Создание новой задачи
                task_serializer = TaskSerializer(data=task_data)
                task_serializer.is_valid(raise_exception=True)
                task_serializer.save(goal=goal_instance)

    def to_representation(self, instance):
        return IdpSerializer(
            instance, context={"request": self.context.get("request")}
        ).data
