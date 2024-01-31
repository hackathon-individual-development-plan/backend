from django.utils.timezone import make_aware

from apps.idps.models import Comment, Goal, Idp, Task
from apps.users.models import ChiefEmployee, Role, User, UserRole


def import_users(obj):
    cells = obj.iter_rows()

    employee_list = []
    for username, fio, job_title, role, photo in cells:
        user_obj, created = User.objects.get_or_create(
            username=username.value,
            fio=fio.value,
            job_title=job_title.value,
            photo=photo.value,
        )
        UserRole.objects.get_or_create(user=user_obj, role=role.value)
        if role.value == Role.CHIEF:
            chief = user_obj
        else:
            employee_list.append(user_obj)
    for employee in employee_list:
        ChiefEmployee.objects.get_or_create(employee=employee, chief=chief)
    print("пользователи загружены")


def import_idps(obj):
    cells = obj.iter_rows()

    for title_idp, employee_idp, chief_idp, status in cells:
        employee = User.objects.get(fio=employee_idp.value)
        chief = User.objects.get(fio=chief_idp.value)
        Idp.objects.get_or_create(
            title=title_idp.value,
            employee=employee,
            chief=chief,
            status=status.value,
        )
    print("ИПР загружены")


def import_goals(obj):
    cells = obj.iter_rows()
    for title_goal, description_id, idp_id, deadline_date in cells:
        idp = Idp.objects.get(title=idp_id.value)

        Goal.objects.get_or_create(
            title=title_goal.value,
            description=description_id.value,
            idp=idp,
            deadline=make_aware(deadline_date.value),
        )
    print("Цели загружены")


def import_tasks(obj):
    cells = obj.iter_rows()

    for text_task, goal in cells:
        goal = Goal.objects.get(title=goal.value)
        Task.objects.get_or_create(text=text_task.value, goal=goal)
    print("Задачи загружены")


def import_comments(obj):
    cells = obj.iter_rows()

    for text_comment, goal_id, user in cells:
        goal = Goal.objects.get(title=goal_id.value)
        user = User.objects.get(fio=user.value)
        Comment.objects.get_or_create(
            comment_text=text_comment.value, goal=goal, user=user
        )
    print("Комментарии загружены")
