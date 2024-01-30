from django.utils.timezone import make_aware
from faker import Faker

from apps.idps.models import Comment, Goal, Idp, Task
from apps.users.models import ChiefEmployee, Role, User, UserRole

fake = Faker()


def import_users(obj):
    cells = obj.iter_rows()

    employee_list = []
    for username, fio, job_title, role, photo in cells:
        user_obj = User.objects.create(
            username=username.value,
            fio=fio.value,
            job_title=job_title.value,
            photo=photo.value,
        )
        UserRole.objects.create(user=user_obj, role=role.value)
        if role.value == Role.CHIEF:
            chief = user_obj
        else:
            employee_list.append(user_obj)
    for employee in employee_list:
        ChiefEmployee.objects.create(employee=employee, chief=chief)
    print("пользователи загружены")


def import_idps(obj):
    cells = obj.iter_rows()

    for id_idp, title_idp, employee_idp, chief_idp, status in cells:
        employee = User.objects.get(id=employee_idp.value)
        chief = User.objects.get(id=chief_idp.value)
        Idp.objects.create(
            id=id_idp.value,
            title=title_idp.value,
            employee=employee,
            chief=chief,
            status=status.value,
        )
    print("ИПР загружены")


def import_goals(obj):
    cells = obj.iter_rows()
    for id_goal, title_goal, description_id, idp_id, deadline_date in cells:
        idp = Idp.objects.get(id=idp_id.value)

        Goal.objects.create(
            id=id_goal.value,
            title=title_goal.value,
            description=description_id.value,
            idp=idp,
            deadline=make_aware(deadline_date.value),
        )
    print("Цели загружены")


def import_tasks(obj):
    cells = obj.iter_rows()

    for text_task, goal_id in cells:
        goal = Goal.objects.get(id=goal_id.value)
        Task.objects.create(text=text_task.value, goal=goal)
    print("Задачи загружены")


def import_comments(obj):
    cells = obj.iter_rows()

    for text_comment, goal_id, user_id in cells:
        goal = Goal.objects.get(id=goal_id.value)
        user = User.objects.get(id=user_id.value)
        Comment.objects.create(
            comment_text=text_comment.value, goal=goal, user=user
        )
    print("Комментарии загружены")
