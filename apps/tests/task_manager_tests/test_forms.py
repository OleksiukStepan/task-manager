from django.test import TestCase
from django.utils import timezone
from apps.task_manager.forms import (
    MemberCreateForm,
    MemberUpdateForm,
    TaskForm,
    SearchForm,
    TaskTypeForm,
    PositionForm,
    TagForm,
)
from apps.task_manager.models import Worker, TaskType, Position, Tag


class MemberCreateFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_member_create_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "test_12345",
            "password2": "test_12345",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "phone": "+12345678910",
            "position": self.position.id,
            "male": True,
            "birthday": timezone.now().date(),
        }
        form = MemberCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_member_create_form_password_mismatch(self):
        form_data = {
            "username": "testuser",
            "password1": "password123",
            "password2": "differentpassword",
        }
        form = MemberCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class MemberUpdateFormTests(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create_user(
            username="testworker",
            password="password123",
            first_name="Test",
            last_name="Worker",
        )

    def test_member_update_form_valid_data(self):
        form_data = {
            "username": "updatedworker",
            "first_name": "Updated",
            "last_name": "Worker",
            "email": "updated@example.com",
        }
        form = MemberUpdateForm(data=form_data, instance=self.worker)
        self.assertTrue(form.is_valid())

    def test_member_update_form_invalid_email(self):
        form_data = {
            "username": "updatedworker",
            "email": "not-an-email",
        }
        form = MemberUpdateForm(data=form_data, instance=self.worker)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class TaskFormTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Development")

    def test_task_form_valid_data(self):
        form_data = {
            "name": "New Task",
            "description": "Task description",
            "deadline": timezone.now().date(),
            "priority": 2,
            "task_type": self.task_type.id,
            "is_complete": False,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_deadline(self):
        form_data = {
            "name": "Task with Past Deadline",
            "deadline": timezone.now().date() - timezone.timedelta(days=1),
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)
        self.assertEqual(
            form.errors["deadline"][0], "The deadline cannot be in the past"
        )


class SearchFormTests(TestCase):
    def test_search_form_with_data(self):
        form = SearchForm(data={"search": "test"})
        self.assertTrue(form.is_valid())

    def test_search_form_empty(self):
        form = SearchForm(data={"search": ""})
        self.assertTrue(form.is_valid())


class TaskTypeFormTests(TestCase):
    def test_task_type_form_valid_data(self):
        form_data = {"name": "Design"}
        form = TaskTypeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_type_form_empty_name(self):
        form_data = {"name": ""}
        form = TaskTypeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class PositionFormTests(TestCase):
    def test_position_form_valid_data(self):
        form_data = {"name": "Manager"}
        form = PositionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_position_form_empty_name(self):
        form_data = {"name": ""}
        form = PositionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TagFormTests(TestCase):
    def test_tag_form_valid_data(self):
        form_data = {"name": "High Priority", "color": "#FF0000"}
        form = TagForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_tag_form_invalid_color(self):
        form_data = {"name": "Urgent", "color": "not-a-color"}
        form = TagForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("color", form.errors)
