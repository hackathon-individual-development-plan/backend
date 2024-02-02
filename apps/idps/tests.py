from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.users.models import User


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

        # Создаем пользователя с ролью Руководитель
        self.chief_user = User.objects.create(
            username="chief_user", fio="ФИО", job_title="Chief"
        )
        self.chief_token = Token.objects.create(user=self.chief_user)
        self.chief_client = APIClient()
        self.chief_client.credentials(
            HTTP_AUTHORIZATION="Token " + self.chief_token.key
        )

    def test_endpoint_create_idps_by_chief(self):
        """Тестирование создания ИПР руководителем."""
        response = self.chief_client.post("/api/v1/idps/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_endpoint_get_idps_by_chief(self):
        """Тестирование получения списка ИПР руководителем."""
        print(self.chief_client.credentials())
        response = self.employee_client.get("/api/v1/idps/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_endpoint_create_idps_by_employee(self):
        """Тестирование создания ИПР сотрудником."""
        response = self.employee_client.get("/api/v1/idps/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_endpoint_get_idps_by_employee(self):
        """Тестирование получения списка сотрудником."""
        print(self.employee_client.credentials())
        response = self.employee_client.get("/api/v1/idps/2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
