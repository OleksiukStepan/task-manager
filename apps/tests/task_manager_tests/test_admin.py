from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from apps.task_manager.models import TaskType, Position, Worker, Task, Tag
from django.utils import timezone


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="adminuser", password="admin123"
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
        self.task = Task.objects.create(
            name="Fix Bug",
            description="Fix a critical bug",
            deadline=timezone.now().date(),
            priority=1,
            task_type=self.task_type,
        )
        self.tag = Tag.objects.create(name="Urgent", color="#FF0000")

    def test_worker_position_in_list_display(self):
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Developer")

    def test_worker_position_in_fieldsets(self):
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        response = self.client.get(url)
        self.assertContains(response, "position")

    def test_task_name_in_list_display(self):
        url = reverse("admin:task_manager_task_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Fix Bug")

    def test_task_filters_in_admin(self):
        url = reverse("admin:task_manager_task_changelist")
        response = self.client.get(url)
        self.assertContains(response, "is_complete")
        self.assertContains(response, "priority")
        self.assertContains(response, "task_type")

    def test_tag_in_list_display(self):
        url = reverse("admin:task_manager_tag_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Urgent")
        self.assertContains(response, "#FF0000")

    def test_task_type_registered_in_admin(self):
        url = reverse("admin:task_manager_tasktype_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Development")

    def test_position_registered_in_admin(self):
        url = reverse("admin:task_manager_position_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Developer")
