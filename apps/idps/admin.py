from django.contrib import admin
from django.contrib.auth.models import Group

from apps.idps.models import Comment, Goal, GoalForIdp, GoalTask, Idp, Task


class GoalTaskAdmin(admin.TabularInline):
    model = GoalTask
    min_num = 1


class GoalForIdpAdmin(admin.TabularInline):
    model = GoalForIdp
    min_num = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    @admin.display(description="Цель")
    def goal_list(self, obj):
        return list(goal.goal for goal in obj.goals.all())

    list_display = ("pk", "text", "goal_list", "created_at")
    search_fields = ("text",)
    list_filter = ("created_at",)
    empty_value_display = "-пусто-"


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    @admin.display(description="Задачи")
    def tasks_list(self, obj):
        return list(task for task in obj.tasks.all())

    list_display = ("pk", "title", "description", "tasks_list", "created_at")
    search_fields = ("title",)
    list_filter = ("created_at", "tasks")
    inlines = [
        GoalTaskAdmin,
    ]
    empty_value_display = "-пусто-"


@admin.register(Idp)
class IdpAdmin(admin.ModelAdmin):
    @admin.display(description="Цели")
    def goal_list(self, obj):
        return list(goal for goal in obj.goals.all())

    list_display = (
        "pk",
        "title",
        "chief",
        "employee",
        "goal_list",
        "status",
        "created_at",
    )
    search_fields = ("title", "chief", "employee", "status")
    list_filter = ("created_at", "chief", "employee", "status")
    inlines = [
        GoalForIdpAdmin,
    ]
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "comment_text",
        "goal_id",
        "user_id",
        "created_at",
    )
    search_fields = ("goal_id", "user_id", "created_at")
    list_filter = ("goal_id", "user_id", "created_at")
    empty_value_display = "-пусто-"


admin.site.unregister(Group)
