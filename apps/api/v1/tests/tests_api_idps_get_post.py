from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.idps.models import Idp
from apps.users.models import ChiefEmployee, Role, User, UserRole


class APITestCase(TestCase):
    def setUp(self):
        # Создаем пользователя с ролью Сотрудник
        self.employee_user = User.objects.create(
            username="employee_user", fio="ФИО", job_title="Employee"
        )
        self.employee_token = Token.objects.create(user=self.employee_user)
        self.employee_client = APIClient()
        self.employee_client.credentials(
            HTTP_AUTHORIZATION="Token " + self.employee_token.key
        )
        self.employee_role = UserRole.objects.create(
            user=self.employee_user, role=Role.EMPLOYEE
        )

        # Создаем пользователя с ролью Руководитель
        self.chief_user = User.objects.create(
            username="chief_user", fio="ФИО", job_title="Chief"
        )
        self.chief_token = Token.objects.create(user=self.chief_user)
        self.chief_client = APIClient()
        self.chief_client.credentials(
            HTTP_AUTHORIZATION="Token " + self.chief_token.key
        )
        self.chief_role = UserRole.objects.create(
            user=self.chief_user, role=Role.CHIEF
        )

        # Создаем связь Руководитель-Сотрудник
        ChiefEmployee.objects.create(
            chief=self.chief_user, employee=self.employee_user
        )

    def test_endpoint_create_idps_by_chief(self):
        """Тестирование создания ИПР руководителем."""
        data = {
            "title": "Test Idps",
            "goals": [
                {
                    "title": "Test Goal",
                    "description": "Test Description",
                    "deadline": "2024-03-08",
                    "tasks": [{"text": "Test Task"}],
                }
            ],
            "employee": self.employee_user.id,
        }
        response = self.chief_client.post(
            "/api/v1/idps/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_endpoint_get_idps_by_chief(self):
        """Тестирование получения ИПР руководителем."""
        idp = Idp.objects.create(
            title="Вырасти до джуна 2",
            employee=self.employee_user,
            chief=self.chief_user,
        )
        response = self.chief_client.get(f"/api/v1/idps/{idp.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(
            data,
            {
                "id": idp.id,
                "title": "Вырасти до джуна 2",
                "status": "В работе",
                "goals": [],
                "employee": {
                    "id": self.employee_user.id,
                    "fio": "ФИО",
                    "job_title": "Employee",
                    "photo": None,
                },
            },
        )

    def test_endpoint_get_idps_by_employee(self):
        """Тестирование получения своего ИПР сотрудником."""
        idp = Idp.objects.create(
            title="Вырасти до джуна 2",
            employee=self.employee_user,
            chief=self.chief_user,
        )
        response = self.employee_client.get(f"/api/v1/idps/{idp.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(
            data,
            {
                "id": idp.id,
                "title": "Вырасти до джуна 2",
                "status": "В работе",
                "goals": [],
                "employee": {
                    "id": self.employee_user.id,
                    "fio": "ФИО",
                    "job_title": "Employee",
                    "photo": None,
                },
            },
        )

    def test_endpoint_create_idps_by_employee(self):
        """Тестирование создания ИПР сотрудником."""
        data = {
            "title": "Test Idps",
            "goals": [
                {
                    "title": "Test Goal",
                    "description": "Test Description",
                    "deadline": "2024-03-08",
                    "tasks": [{"text": "Test Task"}],
                }
            ],
            "employee": self.employee_user.id,
        }
        response = self.employee_client.post(
            "/api/v1/idps/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
