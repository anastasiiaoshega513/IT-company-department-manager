from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import WorkerCreationForm, WorkerUpdateForm, TaskCreateForm, TaskUpdateForm, TaskTypeSearchForm, \
    WorkerSearchForm, PositionSearchForm, TaskSearchForm
from task_manager.models import Task, TaskType, Position


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_of_all_tasks = Task.objects.count()
    num_of_done_tasks = Task.objects.filter(is_completed=True).count()
    num_of_active_tasks = Task.objects.filter(is_completed=False).count()
    num_of_workers = get_user_model().objects.count()
    context = {
        "num_of_all_tasks": num_of_all_tasks,
        "num_of_done_tasks": num_of_done_tasks,
        "num_of_active_tasks": num_of_active_tasks,
        "num_of_workers": num_of_workers,
    }
    return render(request,"task_manager/index.html", context=context)


@login_required
def task_toggle(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        task.is_completed = not task.is_completed
        task.save(update_fields=["is_completed"])
    return redirect(reverse("task_manager:task-list"))

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = context["task_list"]
        context["active_tasks"] = tasks.filter(is_completed=False)
        context["completed_tasks"] = tasks.filter(is_completed=True)

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = (
            Task.objects
            .select_related("task_type")
            .prefetch_related("assignees", "assignees__position")
        )
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        position = self.request.GET.get("position", "")
        context["search_form"] = WorkerSearchForm(
            initial={"position": position}
        )
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(position__name__icontains=form.cleaned_data["position"])
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        context["uncompleted_tasks"] = worker.tasks.filter(is_completed=False)
        context["completed_tasks"] = worker.tasks.filter(is_completed=True)
        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm


class WorkerUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj or self.request.user.is_superuser

class WorkerDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:worker-list")

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj or self.request.user.is_superuser
