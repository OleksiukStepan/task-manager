from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from apps.task_manager.models import Task


# @login_required(login_url="/login/")
def index(request):
    recent_tasks = Task.objects.order_by("-created_at")[:5]
    context = {
        "segment": "index",
        "recent_tasks": recent_tasks,
    }

    html_template = loader.get_template("pages/index.html")
    return HttpResponse(html_template.render(context, request))
