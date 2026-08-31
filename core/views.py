from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Project, Task, Comment


@login_required
def home(request):
    projects = Project.objects.all()

    return render(request, 'core/home.html', {
        'projects': projects
    })


@login_required
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        Project.objects.create(
            name=name,
            description=description
        )

        return redirect('home')

    return render(request, 'core/create_project.html')


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    tasks = project.tasks.all()

    return render(request, 'core/project_detail.html', {
        'project': project,
        'tasks': tasks
    })


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Get all registered users for task assignment
    users = User.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        assigned_to_id = request.POST.get('assigned_to')

        # Default: no user assigned
        assigned_to = None

        # Assign task to selected user
        if assigned_to_id:
            assigned_to = User.objects.get(id=assigned_to_id)

        Task.objects.create(
            project=project,
            title=title,
            description=description,
            status=status,
            assigned_to=assigned_to
        )

        return redirect(
            'project_detail',
            project_id=project.id
        )

    return render(request, 'core/create_task.html', {
        'project': project,
        'users': users
    })


@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        text = request.POST.get('text')

        if text:
            Comment.objects.create(
                task=task,
                user=request.user,
                text=text
            )

    return redirect(
        'project_detail',
        project_id=task.project.id
    )


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'core/login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)

    return redirect('login')