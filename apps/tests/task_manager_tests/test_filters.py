from django.test import TestCase
from django.template import Context, Template
from apps.task_manager.models import Tag


class CustomFilterTests(TestCase):
    def test_priority_class_filter(self):
        template = Template(
            "{% load custom_filters %}{{ 1|priority_class }}"
        )
        rendered = template.render(Context())
        self.assertEqual(rendered, "text-danger")

        template = Template(
            "{% load custom_filters %}{{ 4|priority_class }}"
        )
        rendered = template.render(Context())
        self.assertEqual(rendered, "text-muted")

    def test_load_tags_inclusion_tag(self):
        Tag.objects.create(name="High Priority", color="#FF0000")
        Tag.objects.create(name="Low Priority", color="#00FF00")

        template = Template(
            "{% load custom_filters %}{% load_tags %}"
        )
        rendered = template.render(Context())

        self.assertIn("High Priority", rendered)
        self.assertIn("Low Priority", rendered)
