from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import ChiefEmployee, Role, User, UserRole


class UserTestCase(TestCase):
    """Тестирование модели пользователя"""

    @classmethod
    def setUp(cls):
        User.objects.create(username="user", fio="ФИО", job_title="Должность")

    def test_user_fio(self):
        user = User.objects.get(id=1)
        field = user._meta.get_field("fio").verbose_name
        self.assertEqual(field, "ФИО")

    def test_user_job_title(self):
        user = User.objects.get(id=1)
        field = user._meta.get_field("job_title").verbose_name
        self.assertEqual(field, "Должность")

    def test_user_str(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.__str__(), user.username)


class UserRoleTestCase(TestCase):
    """Тестирование модели связи между пользователями и их ролями"""

    @classmethod
    def setUp(cls):
        user = User.objects.create(
            username="user", fio="ФИО", job_title="Должность"
        )
        UserRole.objects.create(user=user, role=Role.EMPLOYEE)

    def test_user_role_str(self):
        user_role = UserRole.objects.get(id=1)
        expected_str = (
            f"{user_role.user.username} - {user_role.get_role_display()}"
        )
        self.assertEqual(user_role.__str__(), expected_str)


class ChiefEmployeeTestCase(TestCase):
    """Тестирование модели связи м/д руководителями и их сотрудниками"""

    @classmethod
    def setUp(cls):
        chief_user = User.objects.create(
            username="chief_user1", fio="ФИО", job_title="Chief"
        )
        employee_user = User.objects.create(
            username="employee_user1", fio="ФИО", job_title="Employee"
        )
        ChiefEmployee.objects.create(chief=chief_user, employee=employee_user)

    def test_chief_employee_str(self):
        chief_employee = ChiefEmployee.objects.get(id=1)
        expected_str = f"{chief_employee.chief.username} - {chief_employee.employee.username}"
        self.assertEqual(chief_employee.__str__(), expected_str)

    def test_chief_employee_clean(self):
        with self.assertRaises(ValidationError):
            invalid_chief_employee = ChiefEmployee(chief=None, employee=None)
            invalid_chief_employee.full_clean()
