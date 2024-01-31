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

    def test_endpoint_access_employee_my_idp_retrieve(self):
        print(self.chief_client.credentials())
        response = self.employee_client.get("/api/v1/employee/my-idp/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_endpoint_access_employees(self):
        response = self.chief_client.get("/api/v1/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_endpoint_access_employees_without_idp(self):
        response = self.chief_client.get("/api/v1/employees-without-idp/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
