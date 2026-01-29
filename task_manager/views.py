from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from task_manager.models import Task, Worker


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_of_all_tasks = Task.objects.count()
    num_of_done_tasks = Task.objects.filter(is_completed=True).count()
    num_of_active_tasks = Task.objects.filter(is_completed=False).count()
    num_of_workers = Worker.objects.count()
    context = {
        "num_of_all_tasks": num_of_all_tasks,
        "num_of_done_tasks": num_of_done_tasks,
        "num_of_unfinished_tasks": num_of_active_tasks,
        "num_of_workers": num_of_workers,
    }
    return render(request,"task_manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
