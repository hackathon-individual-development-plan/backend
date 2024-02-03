from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.idps.models import Goal, Idp, Task
from apps.users.models import ChiefEmployee, Role, User, UserRole


class APITestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем пользователя с ролью Сотрудник
        cls.employee_user = User.objects.create(
            username="employee_user", fio="ФИО", job_title="Employee"
        )
        cls.employee_token = Token.objects.create(user=cls.employee_user)
        cls.employee_client = APIClient()
        cls.employee_client.credentials(
            HTTP_AUTHORIZATION="Token " + cls.employee_token.key
        )
        cls.employee_role = UserRole.objects.create(
            user=cls.employee_user, role=Role.EMPLOYEE
        )

        # Создаем пользователя с ролью Руководитель
        cls.chief_user = User.objects.create(
            username="chief_user", fio="ФИО", job_title="Chief"
        )
        cls.chief_token = Token.objects.create(user=cls.chief_user)
        cls.chief_client = APIClient()
        cls.chief_client.credentials(
            HTTP_AUTHORIZATION="Token " + cls.chief_token.key
        )
        cls.chief_role = UserRole.objects.create(
            user=cls.chief_user, role=Role.CHIEF
        )

        # Создаем связь Руководитель-Сотрудник
        ChiefEmployee.objects.create(
            chief=cls.chief_user, employee=cls.employee_user
        )

        # Создаем ИПР
        idp = Idp.objects.create(
            title="Test Idps", employee=cls.employee_user, chief=cls.chief_user
        )
        goal = Goal.objects.create(
            title="Test Goal",
            description="Test Description",
            deadline="2024-03-08",
            idp=idp,
        )
        tasks_list = [Task(text=f"Test Task{i}", goal=goal) for i in [1, 2, 3]]
        Task.objects.bulk_create(tasks_list)

    @classmethod
    def tearDownClass(cls):
        pass

    def check_data(
        self,
        title_idp="Test Idps",
        status_idp="Test Status Idp",
        goal_id=1,
        title_goal="Test Title Goal",
        deadline="2024-03-08",
        status_goal="Test Status Goal",
        description_goal="Test Description Goal",
        task1_id=1,
        text_task1="Test Text Task1",
        task2_id=2,
        text_task2="Test Text Task2",
        task3_id=3,
        text_task3="Test Text Task3",
    ):
        return {
            "title": title_idp,
            "status": status_idp,
            "goals": [
                {
                    "id": goal_id,
                    "title": title_goal,
                    "deadline": deadline,
                    "status": status_goal,
                    "description": description_goal,
                    "tasks": [
                        {"id": task1_id, "text": text_task1},
                        {"id": task2_id, "text": text_task2},
                        {"id": task3_id, "text": text_task3},
                    ],
                }
            ],
        }

    def test_endpoint_create_idps_by_chief(self):
        """Тестирование создания ИПР руководителем."""
        data = {
            "title": "Test Idps",
            "goals": [
                {
                    "title": "Test Goal",
                    "description": "Test Description",
                    "deadline": "2024-02-03T14:06:31.104Z",
                    "tasks": [{"text": "Test Task"}],
                }
            ],
            "employee": 1,
        }
        response = self.chief_client.post(
            "/api/v1/idps/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_endpoint_get_idps_by_chief(self):
        """Тестирование получения списка ИПР руководителем."""
        data = self.check_data()
        response = self.chief_client.get(
            "/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_endpoint_get_idps_by_employee(self):
        """Тестирование получения списка сотрудником."""
        data = self.check_data()
        response = self.employee_client.get(
            "/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_endpoint_create_idps_by_employee(self):
        """Тестирование создания ИПР сотрудником."""
        data = self.check_data(
            title_idp="Test Idps",
            status_idp="Test Status Idp",
            goal_id=1,
            title_goal="Test Title Goal",
            deadline="2024-03-08",
            status_goal="Test Status Goal",
            description_goal="Test Description Goal",
            task1_id=1,
            text_task1="Test Text Task1",
            task2_id=2,
            text_task2="Test Text Task2",
            task3_id=3,
            text_task3="Test Text Task3",
        )
        response = self.employee_client.post(
            "/api/v1/idps/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
