from django import template

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
