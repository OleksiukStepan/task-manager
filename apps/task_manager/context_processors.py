from django.urls import resolve, reverse


def breadcrumb_context(request):
    breadcrumbs = []
    current_url_name = resolve(request.path_info).url_name

    if current_url_name == "home":
        breadcrumbs = []

    elif current_url_name == "task_list":
        breadcrumbs = [
            {"name": "Task List", "url": reverse("task_list")},
        ]

    elif current_url_name == "task_detail":
        task_id = request.resolver_match.kwargs.get("pk", "")
        breadcrumbs = [
            {"name": "Task List", "url": reverse("task_list")},
            {"name": task_id, "url": ""},
        ]

    elif current_url_name == "member_list":
        breadcrumbs = [
            {"name": "Member List", "url": reverse("member_list")},
        ]

    return {"breadcrumbs": breadcrumbs}
