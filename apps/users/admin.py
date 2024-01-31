from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import ChiefEmployee, User, UserRole


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    @admin.display(description="Фото")
    def take_image(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src={obj.photo.url} width="80" height="60">'
            )
        return None

    fieldsets = ((None, {"fields": ("fio", "job_title", "photo")}),)

    list_display = ("username", "id", "fio", "job_title", "take_image")
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
