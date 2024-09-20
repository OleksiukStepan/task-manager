from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView

from apps.task_manager.forms import MemberUpdateForm
from apps.task_manager.models import Task, Worker, TaskType


# @login_required(login_url="/login/")
def index(request):
    recent_tasks = Task.objects.order_by("-created_at")[:5]
    team_members = Worker.objects.all()[:5]

    context = {
        "segment": "index",
        "recent_tasks": recent_tasks,
        "team_members": team_members,
    }

    html_template = loader.get_template("pages/index.html")
    return HttpResponse(html_template.render(context, request))


# class TaskListView(LoginRequiredMixin, ListView):
class TaskListView(ListView):
    model = Task
    template_name = "pages/task_list.html"
    context_object_name = "task_list"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.select_related('task_type')
        sort_by = self.request.GET.get('sort_by', 'created_at')
        sort_dir = self.request.GET.get('sort_dir', 'desc')

        if sort_by in ['name', 'deadline', 'created_at', 'priority']:
            order = f'-{sort_by}' if sort_dir == 'desc' else sort_by
            queryset = queryset.order_by(order)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort_by'] = self.request.GET.get(
            'sort_by', 'created_at'
        )
        context['current_sort_dir'] = self.request.GET.get('sort_dir', 'desc')
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "pages/task_detail.html"

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user

        if "Add" in request.POST:
            task.assignees.add(user)
        elif "Delete" in request.POST:
            task.assignees.remove(user)

        return redirect("task_manager:task_detail", pk=task.id)


class MemberListView(ListView):
    model = Worker


class MemberDetailView(DetailView):
    model = Worker
    template_name = "pages/member_detail.html"
    context_object_name = "worker"


class MemberUpdateView(UpdateView):
    model = Worker
    form_class = MemberUpdateForm
    template_name = "pages/member_update.html"
    context_object_name = "worker"

    def get_success_url(self):
        return reverse(
            "task_manager:member_update",
            kwargs={"pk": self.object.pk}
        )
