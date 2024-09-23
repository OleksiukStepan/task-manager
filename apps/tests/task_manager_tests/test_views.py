from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.task_manager.models import Task, Worker, TaskType, Position, Tag
from django.utils import timezone


class TaskManagerViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin123"
        )
        self.client.force_login(self.admin_user)

        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="testworker",
            password="password123",
            first_name="Test",
            last_name="Worker",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(name="Development")
        self.tag = Tag.objects.create(name="Urgent", color="#FF0000")
        self.task = Task.objects.create(
            name="Fix Bug",
            description="Fix the critical bug in the system.",
            deadline=timezone.now().date(),
            priority=1,
            task_type=self.task_type,
        )
        self.task.assignees.add(self.worker)
        self.task.tags.add(self.tag)


class IndexViewTests(TaskManagerViewTests):
    def test_index_view(self):
        response = self.client.get(reverse("task_manager:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task Types")
        self.assertContains(response, "Positions")
        self.assertContains(response, "Tags")


class TaskViewTests(TaskManagerViewTests):
    def test_task_list_view(self):
        response = self.client.get(reverse("task_manager:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_create_view(self):
        form_data = {
            "name": "New Task",
            "description": "New task description",
            "deadline": timezone.now().date(),
            "priority": 2,
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
            "tags": [self.tag.id],
        }
        response = self.client.post(reverse("task_manager:task_create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_view(self):
        form_data = {
            "name": "Updated Task",
            "description": "Updated task description",
            "deadline": timezone.now().date(),
            "priority": 3,
            "task_type": self.task_type.id,
        }
        response = self.client.post(reverse("task_manager:task_update", args=[self.task.id]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_task_delete_view(self):
        response = self.client.post(reverse("task_manager:task_delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name=self.task.name).exists())


class WorkerViewTests(TaskManagerViewTests):
    def test_member_list_view(self):
        response = self.client.get(reverse("task_manager:member_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worker.username)

    def test_member_create_view(self):
        form_data = {
            "username": "newworker",
            "password1": "new_123456",
            "password2": "new_123456",
            "first_name": "New",
            "last_name": "Worker",
            "position": self.position.id,
        }
        response = self.client.post(reverse("task_manager:member_create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Worker.objects.filter(username="newworker").exists())

    def test_member_update_view(self):
        form_data = {
            "username": "updatedworker",
            "first_name": "Updated",
            "last_name": "Worker",
        }
        response = self.client.post(reverse("task_manager:member_update", args=[self.worker.id]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.username, "updatedworker")

    def test_member_delete_view(self):
        response = self.client.post(reverse("task_manager:member_delete", args=[self.worker.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Worker.objects.filter(username=self.worker.username).exists())


class TaskTypeViewTests(TaskManagerViewTests):
    def test_add_task_type_view(self):
        form_data = {"name": "Testing"}
        response = self.client.post(reverse("task_manager:add_task_type"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskType.objects.filter(name="Testing").exists())

    def test_remove_task_type_view(self):
        response = self.client.post(reverse("task_manager:remove_task_type", args=[self.task_type.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(name=self.task_type.name).exists())


class PositionViewTests(TaskManagerViewTests):
    def test_add_position_view(self):
        form_data = {"name": "Manager"}
        response = self.client.post(reverse("task_manager:add_position"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Position.objects.filter(name="Manager").exists())

    def test_remove_position_view(self):
        response = self.client.post(reverse("task_manager:remove_position", args=[self.position.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(name=self.position.name).exists())


