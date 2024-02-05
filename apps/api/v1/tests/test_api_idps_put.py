from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from apps.idps.models import Comment, Goal, Idp, Task
from apps.users.models import ChiefEmployee, Role, User, UserRole


class IdpApiTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя с ролью Сотрудник
        self.employee_user = User.objects.create(
            username="employee", fio="ФИО", job_title="Employee"
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
            username="chief", fio="ФИО", job_title="Chief"
        )
        self.chief_token = Token.objects.create(user=self.chief_user)
        self.chief_client = APIClient()
        self.chief_client.credentials(
            HTTP_AUTHORIZATION="token " + self.chief_token.key
        )
        self.chief_role = UserRole.objects.create(
            user=self.chief_user, role=Role.CHIEF
        )
        # создаем связь руководитель-сотрудник
        ChiefEmployee.objects.create(
            chief=self.chief_user, employee=self.employee_user
        )

        # Создаем ИПР для правки
        self.idp = Idp.objects.create(
            title="ИПР для тестирования",
            employee=self.employee_user,
            chief=self.chief_user,
        )
        self.goal = Goal.objects.create(
            title="Цель для теста",
            description="описание цели для теста ипр",
            deadline="2024-12-31",
            idp=self.idp,
        )
        tasks_list = [
            Task(text=f"Задача{i} для цели", goal=self.goal) for i in [1, 2, 3]
        ]
        self.tasks = Task.objects.bulk_create(tasks_list)
        Comment.objects.create(
            comment_text="Тестовый комментарий",
            goal=self.goal,
            user=self.chief_user,
        )

    def check_data(
        self,
        title_idp="ИПР для тестирования",
        status_idp="В работе",
        goal_id=None,
        title_goal="Цель для теста",
        deadline="2024-12-31",
        status_goal="В работе",
        description_goal="описание цели для теста ипр",
        task1_id=None,
        text_task1="Задача1 для цели",
        task2_id=None,
        text_task2="Задача2 для цели",
        task3_id=None,
        text_task3="Задача3 для цели",
    ):
        if goal_id is None:
            goal_id = self.goal.id
        if task1_id is None:
            task1_id = self.tasks[0].id
        if task2_id is None:
            task2_id = self.tasks[1].id
        if task3_id is None:
            task3_id = self.tasks[2].id

        return dict(
            title=title_idp,
            status=status_idp,
            goals=[
                dict(
                    id=goal_id,
                    title=title_goal,
                    deadline=deadline,
                    status=status_goal,
                    description=description_goal,
                    tasks=[
                        dict(id=task1_id, text=text_task1),
                        dict(id=task2_id, text=text_task2),
                        dict(id=task3_id, text=text_task3),
                    ],
                )
            ],
        )

    def test_put_ids_change(self):
        """Тестирование PUT запроса с правильными данными."""
        data = self.check_data(
            title_idp="new ипр",
            status_idp="Выполнен",
            goal_id=self.goal.id,
            title_goal="new Цель для теста",
            deadline="2024-11-29",
            status_goal="Выполнен",
            description_goal="new описание цели для теста ипр",
            task1_id=self.tasks[1].id,
            text_task1="new Задача2 для цели",
            task2_id=self.tasks[0].id,
            text_task2="new Задача1 для цели",
            task3_id=self.tasks[2].id,
            text_task3="new Задача3 для цели",
        )
        response = self.chief_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_ids_error_idp(self):
        """Тестирование PUT запроса несуществующего ИПР."""
        data = self.check_data()
        response = self.chief_client.put(
            path="/api/v1/idps/2/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_ids_error_goal(self):
        """Тестирование PUT запроса: попытка изменить несуществующую цель."""
        data = self.check_data(goal_id=2)
        response = self.chief_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_ids_error_task(self):
        """Тестирование PUT запроса: Попытка изменить несуществующую задачу."""
        data = self.check_data(task3_id=10)
        response = self.chief_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_ids_new_goal(self):
        """Тестирование PUT запроса: добавление новой цели."""
        data = self.check_data()
        data["goals"].append(
            dict(
                title="new_goal",
                deadline="2025-01-01",
                description="new description",
                tasks=[dict(text="new task")],
            )
        )
        response = self.chief_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Goal.objects.count(), 2)

    def test_put_ids_error_deadline(self):
        """Тестирование PUT запроса: направильная дата дедлайна."""
        data = self.check_data(deadline="2023-12-31")
        response = self.chief_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_ids_new_task(self):
        """Тестирование PUT запроса: добавление новой задачи."""
        data = self.check_data()
        data["goals"][0]["tasks"].append(dict(text="new task"))
        response = self.chief_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 4)

    def test_put_ids_del_task(self):
        """Тестирование PUT запроса: удаление задачи."""
        data = self.check_data()
        data["goals"][0]["tasks"].pop()
        response = self.chief_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 2)

    def test_put_ids_empty_ids(self):
        """Тестирование PUT запроса: удаление всех целей у ИПР."""
        data = self.check_data()
        data["goals"].pop()
        response = self.chief_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_ids_del_goal_new_goal(self):
        """Тестирование PUT запроса: добавление новой цели и удаление старой."""
        data = self.check_data()
        data["goals"].pop()
        data["goals"].append(
            dict(
                title="new_goal",
                deadline="2025-01-01",
                description="new description",
                tasks=[dict(text="new task")],
            )
        )
        response = self.chief_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Goal.objects.count(), 1)

    def test_put_ids_employee(self):
        """Тестирование PUT запроса сотрудником."""
        data = self.check_data()
        response = self.employee_client.put(
            path=f"/api/v1/idps/{self.idp.id}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_in_idps_get(self):
        """Тестирование GET ИПР и проверка комментариев."""
        response = self.chief_client.get(
            f"/api/v1/idps/{self.idp.id}/",
        )
        self.assertEqual(
            "Тестовый комментарий",
            response.data["goals"][0]["comments"][0]["comment_text"],
        )

    def test_comment_post(self):
        """Тестирование POST запроса создание нового комментария."""
        response = self.chief_client.post(
            f"/api/v1/goals/{self.goal.pk}/comments/",
            data=dict(comment_text="Создание второго комментария"),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.all().count(), 2)
