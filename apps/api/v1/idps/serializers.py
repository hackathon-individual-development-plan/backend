from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.api.v1.users.serializers.users import (
    UserFIOSerializer,
    UserSerializer,
)
from apps.idps.models import Comment, GoalForIdp, Idp, Task
from apps.users.models import User


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = (
            "id",
            "text",
        )


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
    tasks = TaskSerializer(source="goals_tasks", many=True, read_only=True)
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

    id = serializers.IntegerField(required=False)

    tasks = TaskSerializer(source="goals_tasks", many=True)

    class Meta:
        model = GoalForIdp
        fields = ("id", "title", "description", "deadline", "tasks")
        # read_only_fields = ("id",)


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
            task["goal_id"] = goal_obj.id
            task_obj, created = Task.objects.get_or_create(task)
            list_of_task.append(task_obj.id)


#        goal_obj.tasks.set(list_of_task)


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
            **validated_data,
            chief=User(id=1)
            # chief=self.context["request"].user
        )
        create_goals_for_idp(goals, idp)
        return idp

    def to_representation(self, instance):
        return IdpSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


# class PatchIdpSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор для изменения ИПР. PUT запрос
#     """

#     goals = PatchGoalForIdpSerializer(many=True)

#     class Meta:
#         model = Idp
#         fields = (
#             "id",
#             "title",
#             "goals",
#             "status",
#         )

#     def update(self, instance, validated_data):
#         """
#         Функция для Put запроса
#         """
#         if instance.chief != self.context["request"].user:
#             raise ValidationError("Исправлять может только автор")

#         idp = get_object_or_404(Idp, id=instance.id)  # Старый ИПР
#         goals = GoalForIdp.objects.filter(idp=idp.id)  # Старые цели

#         new_goals = validated_data.pop("goals")  # новые цели
#         super().update(instance, validated_data)  # обновили ИПР
#         # new_tasks = new_goals.pop("tasks")  # новые таски
#         for goal in goals:
#             Task.objects.filter(goals=goal).delete()
#         print(new_goals)
#         # еще не закончила

#         # return super().update(instance, validated_data)

#     def to_representation(self, instance):
#         return IdpSerializer(
#             instance, context={"request": self.context.get("request")}
#         ).data


# мое class PUTIdpSerializer(serializers.ModelSerializer):
#     goals = PatchGoalForIdpSerializer(many=True)

#     class Meta:
#         model = Idp
#         fields = ("id", "title", "goals", "status")

#     def update(self, instance, validated_data):
#         if instance.chief != self.context["request"].user:
#             raise ValidationError("Исправлять может только автор")

#         idp = get_object_or_404(Idp, id=instance.id)  # Старый ИПР
#         goals_data = validated_data.pop("goals", [])  # новые цели

#         with transaction.atomic():
#             super().update(instance, validated_data)  # обновили ИПР

#             for goal_data in goals_data:
#                 tasks_data = goal_data.pop("tasks", [])  # новые таски

#                 # Создаем или обновляем цель
#                 goal, created = GoalForIdp.objects.update_or_create(
#                     idp=idp,
#                     title=goal_data["title"],
#                     defaults={"description": goal_data["description"], "status": goal_data["status"], "deadline": goal_data["deadline"]},
#                 )

#                 # Создаем или обновляем задачи
#                 tasks = [
#                     Task.objects.create(text=task_data["text"]) for task_data in tasks_data
#                 ]
#                 goal.tasks.set(tasks)

#                 # Устанавливаем связь цели с ИПР
#                 idp.idp_goals.add(goal)

#             # Удаление старых целей и их задач
#             old_goals = GoalForIdp.objects.filter(idp=idp)
#             for old_goal in old_goals:
#                 Task.objects.filter(goals=old_goal).delete()
#             old_goals.delete()


class PUTIdpSerializer(serializers.ModelSerializer):
    goals = PatchGoalForIdpSerializer(source="idp_goals", many=True)

    class Meta:
        model = Idp
        fields = (
            "id",
            "title",
            "goals",
            "status",
        )

    def update(self, instance, validated_data):
        goals_data = validated_data["idp_goals"]
        goals_ids = [
            goal_data.get("id", None)
            for goal_data in goals_data
            if goal_data.get("id", None) is not None
        ]

        instance.idp_goals.exclude(id__in=goals_ids).delete()

        # Обновление существующих целей или создание новых целей
        for goal_data in goals_data:
            goal_id = goal_data.get("id", None)
            tasks_data = goal_data.pop("goals_tasks", [])

            if goal_id is not None:
                # Обновление существующей цели
                goal_instance = get_object_or_404(
                    GoalForIdp, id=goal_id, idp=instance
                )
                goal_serializer = GoalForIdpSerializer(
                    goal_instance, data=goal_data, partial=True
                )
                goal_serializer.is_valid(raise_exception=True)
                goal_serializer.save()

                # Обновление задач для цели
                self.update_or_create_tasks(goal_instance, tasks_data)

            else:
                # Создание новой цели
                goal_serializer = GoalForIdpSerializer(data=goal_data)
                goal_serializer.is_valid(raise_exception=True)
                goal_instance = goal_serializer.save(idp=instance)

                # Создание задач для новой цели
                self.update_or_create_tasks(goal_instance, tasks_data)

        # Удаление целей, которых нет в запросе
        # import pdb; pdb.set_trace()

        # Остальная часть вашей логики, если она есть
        return instance

    def update_or_create_tasks(self, goal_instance, tasks_data):
        tasks_ids = [
            task_data.get("id", None)
            for task_data in tasks_data
            if task_data.get("id", None) is not None
        ]

        import pdb

        pdb.set_trace()
        # Удаление задач, которых нет в запросе
        goal_instance.goals_tasks.exclude(id__in=tasks_ids).delete()

        for task_data in tasks_data:
            task_id = task_data.get("id", None)

            if task_id is not None:
                import pdb

                pdb.set_trace()
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
                # import pdb; pdb.set_trace()
                # Создание новой задачи
                task_serializer = TaskSerializer(data=task_data)
                task_serializer.is_valid(raise_exception=True)
                task_serializer.save(goal=goal_instance)
