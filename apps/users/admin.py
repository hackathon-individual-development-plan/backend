from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ChiefEmployee, User, UserRole


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = ((None, {"fields": ("fio", "job_title")}),)
    list_display = (
        "id",
        "username",
        "fio",
        "job_title",
    )
    empty_value_display = "-empty-"


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
    )
    empty_value_display = "-empty-"


@admin.register(ChiefEmployee)
class ChiefEmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "chief",
        "employee",
    )
    empty_value_display = "-empty-"
