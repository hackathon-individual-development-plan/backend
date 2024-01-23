from rest_framework import serializers

from apps.api.v1.users.serializers.users import UserSerializer
from apps.idps.models import Goal, GoalForIdp, GoalTask, Idp, Task
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


class PostGoalForIdpSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)
    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = GoalForIdp
        fields = ("title", "description", "deadline", "tasks")


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


# TODO добавить комменты


class PostIdpSerializer(serializers.ModelSerializer):
    goals = PostGoalForIdpSerializer(many=True)
    employee = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="id"
    )

    class Meta:
        model = Idp
        fields = ("title", "goals", "employee", "chief")
        read_only_fields = ("chief",)

    def create_tasks_for_goal(self, tasks, goal):
        list_of_task = [Task(text=task["text"]) for task in tasks]
        list_of_task_obj = Task.objects.bulk_create(list_of_task)
        list_of_goaltask = [
            GoalTask(goal_id=goal.id, tasks=task) for task in list_of_task_obj
        ]
        GoalTask.objects.bulk_create(list_of_goaltask)

    def create_goals_for_idp(self, goals, idp):
        list_of_goal_for_ipr = []
        for goal in goals:
            tasks = goal.pop("tasks")
            deadline = goal.pop("deadline")
            new_goal, created = Goal.objects.get_or_create(**goal)
            self.create_tasks_for_goal(tasks, new_goal)
            list_of_goal_for_ipr.append(
                GoalForIdp(
                    goal_id=new_goal.pk, deadline=deadline, idp_id=idp.pk
                )
            )
        GoalForIdp.objects.bulk_create(list_of_goal_for_ipr)

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
