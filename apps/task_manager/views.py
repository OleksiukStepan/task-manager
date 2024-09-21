from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from apps.task_manager.forms import (
    MemberUpdateForm,
    TaskTypeForm,
    PositionForm,
    TaskForm,
)
from apps.task_manager.models import Task, Worker, TaskType, Position


# @login_required(login_url="/login/")
def index(request):
    recent_tasks = Task.objects.order_by("-created_at")[:10]
    team_members = Worker.objects.all()[:10]
    task_types = TaskType.objects.all().order_by("name")
    positions = Position.objects.all().order_by("name")
    task_types_form = TaskTypeForm()
    position_form = PositionForm()

    # Handle form submissions based on form_type
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # Handle adding a new task type
        if form_type == "add_task_type":
            task_type_form = TaskTypeForm(request.POST)
            if task_type_form.is_valid():
                task_type_form.save()

        # Handle adding a new position
        elif form_type == "add_position":
            position_form = PositionForm(request.POST)
            if position_form.is_valid():
                position_form.save()

        # Handle removing a task type
        elif "remove_task_type" in request.POST:
            task_type_id = request.POST.get("remove_task_type")
            task_type = get_object_or_404(TaskType, pk=task_type_id)
            task_type.delete()

        # Handle removing a position
        elif "remove_position" in request.POST:
            position_id = request.POST.get("remove_position")
            position = get_object_or_404(Position, pk=position_id)
            position.delete()

        return redirect("task_manager:home")

    context = {
        "segment": "index",
        "recent_tasks": recent_tasks,
        "team_members": team_members,
        "task_types": task_types,
        "positions": positions,
        "task_types_form": task_types_form,
        "position_form": position_form,
    }
    return render(request, "pages/index.html", context)


# class TaskListView(LoginRequiredMixin, ListView):
class TaskListView(ListView):
    model = Task
    template_name = "pages/task_list.html"
    context_object_name = "task_list"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        sort_by = self.request.GET.get("sort_by", "created_at")
        sort_dir = self.request.GET.get("sort_dir", "desc")

        if sort_by in ["name", "deadline", "created_at", "priority"]:
            order = f"-{sort_by}" if sort_dir == "desc" else sort_by
            queryset = queryset.order_by(order)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_sort_by"] = self.request.GET.get("sort_by", "created_at")
        context["current_sort_dir"] = self.request.GET.get("sort_dir", "desc")
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


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "pages/task_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Task"
        return context


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "pages/task_delete.html"
    success_url = reverse_lazy("task_manager:task_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Task"
        return context


class MemberListView(ListView):
    model = Worker
    template_name = "pages/member_list.html"
    context_object_name = 'workers'

    def get_queryset(self):
        return Worker.objects.prefetch_related("tasks")


class MemberDetailView(DetailView):
    model = Worker
    template_name = "pages/member_detail.html"
    context_object_name = "worker"

    def get_queryset(self):
        return Worker.objects.prefetch_related("tasks")


class MemberUpdateView(UpdateView):
    model = Worker
    form_class = MemberUpdateForm
    template_name = "pages/member_update.html"
    context_object_name = "worker"


class MemberDeleteView(DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:member_list")
    template_name = "pages/member_delete.html"
