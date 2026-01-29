from django.urls import path
from .views import (
    index,
    TaskListView,
    TaskDetailView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
)
urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    # path("tasks/create/", TaskDetailView.as_view(), name="task-detail"),
    # path("tasks/<int:pk>/update/", TaskDetailView.as_view(), name="task-detail"),
    # path("tasks/<int:pk>/delete/", TaskDetailView.as_view(), name="task-detail"), future update-create-delete
    path("task_types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task_types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task_types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task_types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
]


app_name = "task_manager"