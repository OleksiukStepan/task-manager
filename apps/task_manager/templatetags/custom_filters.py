from django import template

from apps.task_manager.models import Tag

register = template.Library()


@register.filter
def priority_class(priority):
    if priority == 1:
        return "text-danger"
    elif priority == 2:
        return "text-warning"
    elif priority == 3:
        return "text-info"
    else:
        return "text-muted"


@register.inclusion_tag("includes/tags_list.html")
def load_tags():
    tags = Tag.objects.all()
    return {"tags": tags}
