import nested_admin
from django.contrib import admin
from django.contrib.auth.models import Group

from apps.idps.models import Comment, Goal, Idp, Task


class TaskForIprAdmin(nested_admin.NestedTabularInline):
    model = Task
    fields = ["text"]
    min_num = 1
    extra = 0


class GoalForIprAdmin(nested_admin.NestedStackedInline):
    model = Goal
    min_num = 1
    extra = 0
    inlines = [TaskForIprAdmin]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "goal_id", "created_at")
    search_fields = ("text",)
    list_filter = (
        "goal__title",
        "created_at",
    )
    empty_value_display = "-пусто-"


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    @admin.display(description="Задачи")
    def tasks_list(self, obj):
        return list(task.id for task in obj.goals_tasks.all())

    list_display = (
        "id",
        "title",
        "description",
        "status",
        "tasks_list",
        "deadline",
        "idp_id",
    )
    list_filter = ("idp", "deadline", "created_at", "status")
    empty_value_display = "-пусто-"
    exclude = ("finished_at",)


@admin.register(Idp)
class IdpAdmin(nested_admin.NestedModelAdmin):
    @admin.display(description="Цели")
    def goals_list(self, obj):
        return list(goal.id for goal in obj.idp_goals.all())

    list_display = (
        "title",
        "pk",
        "employee",
        "chief",
        "goals_list",
        "status",
        "created_at",
        "finished_at",
    )
    search_fields = ("title", "chief", "employee", "status")
    list_filter = ("created_at", "chief", "employee", "status")
    inlines = [GoalForIprAdmin]
    exclude = ("finished_at",)
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "comment_text",
        "goal_id",
        "user",
        "created_at",
    )
    search_fields = ("goal", "user", "created_at")
    list_filter = ("goal", "user", "created_at")
    empty_value_display = "-пусто-"


admin.site.unregister(Group)
