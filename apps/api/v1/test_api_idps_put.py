from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from apps.idps.models import Goal, Idp, Task
from apps.users.models import ChiefEmployee, Role, User, UserRole


class IdpApiTestCase(APITestCase):
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
            HTTP_AUTHORIZATION="token " + cls.chief_token.key
        )
        cls.chief_role = UserRole.objects.create(
            user=cls.chief_user, role=Role.CHIEF
        )
        # создаем связь руководитель-сотрудник
        ChiefEmployee.objects.create(
            chief=cls.chief_user, employee=cls.employee_user
        )

        # Создаем ИПР для правки
        idp = Idp.objects.create(
            title="ИПР для тестирования",
            employee=cls.employee_user,
            chief=cls.chief_user,
        )
        print(idp)
        goal = Goal.objects.create(
            title="Цель для теста",
            description="описание цели для теста ипр",
            deadline="2024-12-31",
            idp=idp,
        )
        print(goal)
        tasks_list = [
            Task(text=f"Задача{i} для цели", goal=goal) for i in [1, 2, 3]
        ]
        Task.objects.bulk_create(tasks_list)
        print(tasks_list)

    @classmethod
    def tearDownClass(cls):
        pass

    def check_data(
        self,
        title_idp="ИПР для тестирования",
        status_idp="В работе",
        goal_id=1,
        title_goal="Цель для теста",
        deadline="2024-12-31",
        status_goal="В работе",
        description_goal="описание цели для теста ипр",
        task1_id=1,
        text_task1="Задача1 для цели",
        task2_id=2,
        text_task2="Задача2 для цели",
        task3_id=3,
        text_task3="Задача3 для цели",
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

    # def test_endpoint_access_employee_my_idp_retrieve(self):
    #     response = self.employee_client.get("/api/v1/employee/my-idp/")
    #     print(response)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_endpoint_access_employees(self):
    #     response = self.chief_client.get("/api/v1/employees/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_endpoint_access_employees_without_idp(self):
    #     response = self.chief_client.get("/api/v1/employees-without-idp/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_ids_change(self):
        data = self.check_data(
            title_idp="new ипр",
            status_idp="Выполнен",
            goal_id=1,
            title_goal="new Цель для теста",
            deadline="2024-11-29",
            status_goal="Выполнен",
            description_goal="new описание цели для теста ипр",
            task1_id=2,
            text_task1="new Задача2 для цели",
            task2_id=1,
            text_task2="new Задача1 для цели",
            task3_id=3,
            text_task3="new Задача3 для цели",
        )
        response = self.chief_client.put(
            path="/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_ids_error_idp(self):
        data = self.check_data()
        response = self.chief_client.put(
            path="/api/v1/idps/2/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_ids_error_goal(self):
        data = self.check_data(goal_id=2)
        response = self.chief_client.put(
            path="/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_ids_error_task(self):
        data = self.check_data(task3_id=10)
        response = self.chief_client.put(
            path="/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_ids_new_goal(self):
        data = self.check_data()
        data["goals"].append(
            {
                "title": "new_goal",
                "deadline": "2025-01-01",
                "description": "new description",
                "tasks": [{"text": "new task"}],
            }
        )
        response = self.chief_client.put(
            path="/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Goal.objects.count(), 2)

    def test_put_ids_new_task(self):
        data = self.check_data()
        data["goals"][0]["tasks"].append({"text": "new task"})
        response = self.chief_client.put(
            path="/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 4)

    def test_put_ids_del_task(self):
        data = self.check_data()
        data["goals"][0]["tasks"].pop()
        response = self.chief_client.put(
            path="/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 2)

    def test_put_ids_empty_ids(self):
        data = self.check_data()
        data["goals"].pop()
        response = self.chief_client.put(
            path="/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_ids_del_goal_new_goal(self):
        data = self.check_data()
        data["goals"].pop()
        data["goals"].append(
            {
                "title": "new_goal",
                "deadline": "2025-01-01",
                "description": "new description",
                "tasks": [{"text": "new task"}],
            }
        )
        response = self.chief_client.put(
            path="/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Goal.objects.count(), 1)

    def test_put_ids_employee(self):
        data = self.check_data()
        response = self.employee_client.put(
            path="/api/v1/idps/1/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
