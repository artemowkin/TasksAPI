from django.urls import path

from . import views


urlpatterns = [
    path('', views.AllCreateTasksView.as_view(), name='all_create_tasks'),
    path('<uuid:pk>/', views.DeleteTaskView.as_view(), name='delete_task'),
]

