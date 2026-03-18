from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from core.models import Task, Status


def index(request):
    tasks = Task.objects.all().order_by('-created_at')

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    # Status Filter
    if status_filter == 'active':
        tasks = tasks.filter(status=Status.ACTIVE)
    elif status_filter == 'completed':
        tasks = tasks.filter(status=Status.COMPLETED)

    # Priority Filter
    if priority_filter == 'high':
        tasks = tasks.filter(priority='High')
    elif priority_filter == 'medium':
        tasks = tasks.filter(priority='Medium')
    elif priority_filter == 'low':
        tasks = tasks.filter(priority='Low')

    context = {
        'tasks': tasks,
        'total_count': Task.objects.count(),
        'active_count': Task.objects.filter(status=Status.ACTIVE).count(),
        'completed_count': Task.objects.filter(status=Status.COMPLETED).count(),
        'now': timezone.now(),
        'current_status': status_filter,
        'current_priority': priority_filter,
    }

    return render(request, 'index.html', context)


def create_task(request):
    if request.method == 'POST':
        tags_raw = request.POST.get('tags')
        clean_tags = ",".join([t.strip() for t in tags_raw.split(',')]) if tags_raw else ""

        Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority'),
            status=Status.ACTIVE,
            due_date=request.POST.get('due_date') or None,
            tags=clean_tags,
)
        return redirect('index')

    return render(request, 'task_create.html')


def detail_task(request, id):
    task = get_object_or_404(Task, id=id)

    tags_list = []
    if task.tags:
        tags_list = [t.strip() for t in task.tags.split(',')]

    context = {
        'task': task,
        'tags_list': tags_list
    }

    return render(request, 'task_detail.html', context)


def edit_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        task.due_date = request.POST.get('due_date') or None
        tags_raw = request.POST.get('tags')
        task.tags = ",".join([t.strip() for t in tags_raw.split(',')]) if tags_raw else ""
        task.save()
        return redirect('detail_task', id=task.id)

    return render(request, 'task_edit.html', {'task': task})


def delete_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        task.delete()
        return redirect('index')

    return render(request, 'task_delete.html', {'task': task})


def complete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.status = Status.COMPLETED
    task.save()
    return redirect('index')