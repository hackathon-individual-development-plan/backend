from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.users.models import Role, UserRole

from .models import ChiefEmployee, Goal, Idp, Status, Task, User

# from apps.api.v1.validators import deadline_validator


class IdpTestCase(TestCase):
    """Тестирование модели ИПР."""

    @classmethod
    def setUp(cls):
        cls.chief = User.objects.create(
            username="chief", fio="ФИО 1", job_title="Руководитель IT отдела"
        )
        cls.employee = User.objects.create(
            username="employee", fio="ФИО 2", job_title="Сотрудник IT отдела"
        )
        UserRole.objects.create(user=cls.chief, role=Role.CHIEF)
        UserRole.objects.create(user=cls.employee, role=Role.EMPLOYEE)
        ChiefEmployee.objects.create(chief=cls.chief, employee=cls.employee)

        cls.second_chief = User.objects.create(
            username="secondchief", fio="ФИО 3", job_title="Шеф-повар"
        )
        cls.second_employee = User.objects.create(
            username="secondemployee", fio="ФИО 4", job_title="Повар"
        )
        UserRole.objects.create(user=cls.second_employee, role=Role.EMPLOYEE)
        UserRole.objects.create(user=cls.second_chief, role=Role.CHIEF)

    def test_idp_create(self):
        """Тестирование создания ИПР, цели и задачи."""

        idp = Idp.objects.create(
            title="Вырасти до джуна",
            employee=self.employee,
            chief=self.chief,
        )
        self.assertEqual(idp.title, "Вырасти до джуна")
        self.assertEqual(idp.employee, self.employee)
        self.assertEqual(idp.chief, self.chief)
        self.assertEqual(idp.status, Status.IN_PROGRESS)

        goal = Goal.objects.create(
            title="Научиться писать тесты",
            description="Много и самых разных",
            deadline=datetime.now() + timedelta(days=30),
            idp=idp,
        )
        self.assertEqual(goal.title, "Научиться писать тесты")
        self.assertEqual(goal.description, "Много и самых разных")
        self.assertEqual(goal.status, Status.IN_PROGRESS)
        self.assertEqual(goal.idp, idp)

        task = Task.objects.create(
            text="Познакомиться с библиотекой django.test",
            goal=goal,
        )
        self.assertEqual(task.text, "Познакомиться с библиотекой django.test")
        self.assertEqual(task.goal, goal)

    def test_idp_role_validation(self):
        """Тестирование невозможности создания ИПР сотрудником сотруднику."""

        with self.assertRaises(ValidationError) as context:
            idp = Idp.objects.create(
                title="Вырасти до джуна 2",
                employee=self.employee,
                chief=self.second_employee,
            )
            idp.clean()

        self.assertEqual(
            str(context.exception),
            "['Руководитель должен иметь соответствующую роль!']",
        )

    def test_idp_selffollow_validation(self):
        """Тестирование невозможности создания ИПР самому себе."""

        with self.assertRaises(IntegrityError) as context:
            Idp.objects.create(
                title="Вырасти до джуна 2",
                employee=self.second_chief,
                chief=self.second_chief,
            )

        self.assertIn(
            'violates check constraint "self_follow"', str(context.exception)
        )

    def test_idp_chiefemployee_validation(self):
        """Тестирование невозможности создания ИПР чужому сотруднику."""

        with self.assertRaises(ValidationError) as context:
            idp = Idp.objects.create(
                title="Вырасти до джуна 2",
                employee=self.second_employee,
                chief=self.second_chief,
            )
            idp.clean()

        self.assertEqual(
            str(context.exception), "['Возможно это не ваш сотрудник?']"
        )

    def test_idp_existing_in_progress(self):
        """Тестирование невозможности создания ИПР сотруднику,
        у которого уже есть ИПР в работе."""

        Idp.objects.create(
            title="Существующий ИПР",
            employee=self.employee,
            chief=self.chief,
        )

        with self.assertRaises(ValidationError) as context:
            idp = Idp.objects.create(
                title="Второй ИПР",
                employee=self.employee,
                chief=self.chief,
            )
            idp.clean()

        self.assertEqual(
            str(context.exception),
            "[\"У сотрудника уже есть ИПР со статусом 'В работе'\"]",
        )

    # def test_deadline_validator(self):
    #     idp = Idp.objects.create(
    #             title="Вырасти до джуна 2",
    #             employee=self.employee,
    #             chief=self.chief
    #         )
    #     goal = Goal(
    #         title="Тестовая цель",
    #         description="Тестовое описание",
    #         deadline=datetime.now() - timedelta(days=30),
    #         idp=idp
    #     )
    #     with self.assertRaises(ValidationError) as context:
    #         deadline_validator(goal.deadline)

    #     expected_error_message = "Дата дедлайна должна быть больше, чем сейчас хотя бы на один день"
    #     self.assertEqual(str(context.exception), expected_error_message)
