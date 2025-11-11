from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
import logging

logger = logging.getLogger(__name__)

def list_tasks(request):
    q = request.GET.get('q', '').strip()
    filter_status = request.GET.get('status', 'all') or 'all'
    filter_status = filter_status.strip().lower()

    # debug output in terminal
    print("DEBUG list_tasks: q=%r status=%r" % (q, filter_status))
    logger.info("list_tasks called — q=%r, status=%r", q, filter_status)

    tasks = Task.objects.all().order_by('-created_at')
    if q:
        tasks = tasks.filter(title__icontains=q)

    if filter_status == 'pending':
        tasks = tasks.filter(completed=False)
    elif filter_status == 'done':
        tasks = tasks.filter(completed=True)

    context = {'tasks': tasks, 'q': q, 'filter_status': filter_status}
    return render(request, 'tasks/index.html', context)


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})


def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:list')
    return render(request, 'tasks/confirm_delete.html', {'task': task})


def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('tasks:list')
