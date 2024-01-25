from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.api.v1.users.serializers.users import (
    UserFIOSerializer,
    UserSerializer,
)
from apps.idps.models import Comment, Goal, GoalForIdp, GoalTask, Idp, Task
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


class GoalTaskSerializer(serializers.ModelSerializer):
    text = serializers.ReadOnlyField(source="tasks.text")

    class Meta:
        model = GoalForIdp
        fields = ("text",)


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
    id = serializers.ReadOnlyField(source="goal.id")
    title = serializers.ReadOnlyField(source="goal.title")
    description = serializers.ReadOnlyField(source="goal.description")
    tasks = serializers.SerializerMethodField()
    comments = CommentSerializer(
        source="goal_comment", many=True, read_only=True
    )

    def get_tasks(self, obj):
        return GoalTaskSerializer(
            GoalTask.objects.filter(goal=obj.goal), many=True
        ).data

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
    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = GoalForIdp
        fields = ("title", "description", "deadline", "tasks")


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


# TODO добавить комменты


def create_goals_for_idp(goals, idp):
    """
    Функция создания целей для ИПР в БД
    """
    list_of_goal_for_ipr = []
    for goal in goals:
        tasks = goal.pop("tasks")
        list_of_task = [Task(text=task["text"]) for task in tasks]
        list_of_task_obj = Task.objects.bulk_create(list_of_task)
        deadline = goal.pop("deadline")
        goal_obj, created = Goal.objects.get_or_create(**goal)
        goal_obj.tasks.set(list_of_task_obj)
        list_of_goal_for_ipr.append(
            GoalForIdp(goal_id=goal_obj.pk, deadline=deadline, idp_id=idp.pk)
        )
    GoalForIdp.objects.bulk_create(list_of_goal_for_ipr)


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


class PutIdpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения ИПР. PUT запрос
    """

    goals = PostGoalForIdpSerializer(many=True)

    class Meta:
        model = Idp
        fields = (
            "title",
            "goals",
            "status",
        )

    def delete_goals_tasks_of_idp(self, goals, instance):
        """
        Функция удаления задач и целей при изменении ИПР. PUT запрос.
        """
        task_for_delete = []
        for goal in goals:
            tasks = GoalTask.objects.filter(goal=goal.goal_id)
            task_for_delete.append([task.id for task in tasks])
            Goal.objects.filter(id=goal.goal_id).delete()
        task_for_delete = sum(task_for_delete, [])
        for id in task_for_delete:
            Task.objects.filter(id=id).delete()

    def update(self, instance, validated_data):
        """
        Функция для Put запроса
        """
        if instance.chief != self.context["request"].user:
            raise ValidationError("Исправлять может только автор")

        goals = GoalForIdp.objects.filter(idp=instance)
        self.delete_goals_tasks_of_idp(goals, instance)
        new_goals = validated_data.pop("goals")
        create_goals_for_idp(new_goals, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return IdpSerializer(
            instance, context={"request": self.context.get("request")}
        ).data
