from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
)

from apps.task_manager.forms import (
    MemberCreateForm,
    MemberUpdateForm,
    PositionForm,
    TaskTypeForm,
    TaskForm,
    SearchForm,
    TagForm,
)
from apps.task_manager.models import Task, Worker, TaskType, Position, Tag


# @login_required(login_url="/login/")
def index(request):
    recent_tasks, team_members, task_types, positions, tags = fetch_data()
    task_types_form, position_form, tag_form, search_form = initialize_forms(request)

    search_term = request.GET.get("search", "")
    if search_term:
        recent_tasks, team_members = search_tasks_and_members(search_term)

    context = {
        "segment": "index",
        "recent_tasks": recent_tasks,
        "team_members": team_members,
        "task_types": task_types,
        "positions": positions,
        "tags": tags,
        "task_types_form": task_types_form,
        "position_form": position_form,
        "search_form": search_form,
        "tag_form": tag_form,
    }
    return render(request, "pages/index.html", context)


def fetch_data():
    """Fetches the data needed for the index page."""
    recent_tasks = Task.objects.order_by("-created_at")[:10]
    team_members = Worker.objects.all()[:10]
    task_types = TaskType.objects.all().order_by("name")
    positions = Position.objects.all().order_by("name")
    tags = Tag.objects.all()
    return recent_tasks, team_members, task_types, positions, tags


def initialize_forms(request):
    """Initializes the forms for task types, positions, and tags."""
    task_types_form = TaskTypeForm()
    position_form = PositionForm()
    tag_form = TagForm()
    search_term = request.GET.get("search", "")
    search_form = SearchForm(initial={"search": search_term})
    return task_types_form, position_form, tag_form, search_form


def search_tasks_and_members(search_term):
    """Handles search functionality for tasks and team members."""
    recent_tasks = Task.objects.filter(name__icontains=search_term)
    team_members = Worker.objects.filter(
        Q(username__icontains=search_term)
        | Q(first_name__icontains=search_term)
        | Q(last_name__icontains=search_term)
    )
    return recent_tasks, team_members


def add_task_type(request):
    if request.method == "POST":
        form = TaskTypeForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("task_manager:home")


def remove_task_type(request, task_type_id):
    task_type = get_object_or_404(TaskType, pk=task_type_id)
    task_type.delete()
    return redirect("task_manager:home")


def add_position(request):
    if request.method == "POST":
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("task_manager:home")


def remove_position(request, position_id):
    position = get_object_or_404(Position, pk=position_id)
    position.delete()
    return redirect("task_manager:home")


def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("task_manager:home")


# @login_required
def set_worker_status(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    status = request.GET.get("status", "offline")
    worker.is_online = True if status == "online" else False
    worker.save(update_fields=["is_online"])
    messages.success(
        request,
        (f"Worker status set to " f"{'Online' if worker.is_online else 'Offline'}."),
    )

    return redirect(request.META.get("HTTP_REFERER", "index"))


class SaveTagsView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        selected_tags = request.POST.getlist("tags")
        task.tags.set(selected_tags)  # Set the selected tags to the task
        return redirect("task_manager:task_update", pk=task.pk)


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
        form = SearchForm(self.request.GET)

        if sort_by in ["name", "deadline", "created_at", "priority"]:
            order = f"-{sort_by}" if sort_dir == "desc" else sort_by
            queryset = queryset.order_by(order)

        if form.is_valid() and form.cleaned_data.get("search"):
            queryset = queryset.filter(name__icontains=form.cleaned_data["search"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_sort_by"] = self.request.GET.get("sort_by", "created_at")
        context["current_sort_dir"] = self.request.GET.get("sort_dir", "desc")
        search_term = self.request.GET.get("search", "")
        context["search_form"] = SearchForm(initial={"search": search_term})
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "pages/task_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context["workers"] = Worker.objects.all()
        context["tags"] = task.tags.all()
        context["title"] = "Task Detail"
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user

        # Handling adding and removing members
        if "Add" in request.POST:
            task.assignees.add(user)
        elif "Delete" in request.POST:
            task.assignees.remove(user)

        # Handling saving tags only when the Save Tags button is clicked
        if "save_tags" in request.POST:
            selected_tags = request.POST.getlist("tags")
            task.tags.set(selected_tags)

        return redirect("task_manager:task_detail", pk=task.id)


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "pages/task_create.html"

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        workers = Worker.objects.all()
        return render(
            request, "pages/task_create.html", {"form": form, "workers": workers}
        )

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            member_ids = request.POST.getlist("members")
            members = Worker.objects.filter(id__in=member_ids)
            task.assignees.set(members)
            task.save()
            return redirect("task_manager:task_list")

        workers = Worker.objects.all()
        return render(
            request, "pages/task_create.html", {"form": form, "workers": workers}
        )


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "pages/task_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workers"] = Worker.objects.all()
        context["tags"] = Tag.objects.all()
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
    context_object_name = "workers"
    paginate_by = 10

    def get_queryset(self):
        queryset = Worker.objects.select_related("position").prefetch_related("tasks")
        sort_by = self.request.GET.get("sort_by", "username")
        sort_dir = self.request.GET.get("sort_dir", "desc")
        form = SearchForm(self.request.GET)

        if sort_by in ["username"]:
            order = f"-{sort_by}" if sort_dir == "desc" else sort_by
            queryset = queryset.order_by(order)

        if form.is_valid() and form.cleaned_data.get("search"):
            search_term = form.cleaned_data["search"]
            queryset = queryset.filter(
                Q(username__icontains=search_term)
                | Q(first_name__icontains=search_term)
                | Q(last_name__icontains=search_term)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_sort_by"] = self.request.GET.get("sort_by", "name")
        context["current_sort_dir"] = self.request.GET.get("sort_dir", "desc")
        search_term = self.request.GET.get("search", "")
        context["search_form"] = SearchForm(initial={"search": search_term})
        return context


class MemberCreateView(CreateView):
    model = Worker
    form_class = MemberCreateForm
    template_name = "pages/member_create.html"
    success_url = reverse_lazy("task_manager:member_list")


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
