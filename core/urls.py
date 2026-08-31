from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'create-project/',
        views.create_project,
        name='create_project'
    ),

    path(
        'project/<int:project_id>/',
        views.project_detail,
        name='project_detail'
    ),

    path(
        'project/<int:project_id>/create-task/',
        views.create_task,
        name='create_task'
    ),

    path(
        'task/<int:task_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
]