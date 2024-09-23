from django.test import TestCase
from django.utils import timezone
from apps.task_manager.models import TaskType, Position, Worker, Tag, Task


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="Development")
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="testworker",
            password="password123",
            first_name="Test",
            last_name="Worker",
            position=self.position,
        )
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

    def test_task_type_str(self) -> None:
        self.assertEqual(str(self.task_type), "Development")

    def test_position_str(self) -> None:
        self.assertEqual(str(self.position), "Developer")

    def test_worker_str(self) -> None:
        self.assertEqual(str(self.worker), "testworker (Test Worker)")

    def test_tag_str(self) -> None:
        self.assertEqual(str(self.tag), "Urgent")

    def test_task_str(self) -> None:
        self.assertEqual(str(self.task), "Fix Bug")

    def test_worker_absolute_url(self) -> None:
        self.assertEqual(
            self.worker.get_absolute_url(),
            f"/members/{self.worker.id}/",
        )

    def test_task_absolute_url(self) -> None:
        self.assertEqual(
            self.task.get_absolute_url(),
            f"/tasks/{self.task.id}/",
        )

    def test_task_with_multiple_assignees(self) -> None:
        worker2 = Worker.objects.create_user(
            username="testworker2",
            password="password1234",
            first_name="Test2",
            last_name="Worker2",
            position=self.position,
        )
        self.task.assignees.add(worker2)
        self.assertEqual(self.task.assignees.count(), 2)
        self.assertIn(self.worker, self.task.assignees.all())
        self.assertIn(worker2, self.task.assignees.all())

    def test_task_with_multiple_tags(self) -> None:
        tag2 = Tag.objects.create(name="High Priority", color="#FF9900")
        self.task.tags.add(tag2)
        self.assertEqual(self.task.tags.count(), 2)
        self.assertIn(self.tag, self.task.tags.all())
        self.assertIn(tag2, self.task.tags.all())
