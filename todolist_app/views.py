from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from todolist_app.forms import TaskForm
from todolist_app.models import TaskList


# Create your views here.
@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                (
                    "New Task '{0}' Added!".format(
                        form.cleaned_data["task"],
                    )
                ),
            )
        else:
            messages.warning(request, ("Please Write your task before adding..."))
        return redirect("todolist")
    else:
        all_tasks = TaskList.objects.all()

        paginator = Paginator(all_tasks, 4)
        page = request.GET.get("pg")
        all_tasks = paginator.get_page(page)

        context = {"all_tasks": all_tasks}
        return render(request, "todolist.html", context)


@login_required
def change_status(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = not task.done
    task.save()

    messages.error(
        request,
        (
            "Task -> {0} status is Updated".format(
                task.task,
            )
        ),
    )
    return redirect("todolist")


@login_required
def edit_task(request, task_id):
    task_obj = TaskList.objects.get(pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST or None, instance=task_obj)
        if form.is_valid():
            form.save()
            messages.success(request, ("Task Edited!"))

        return redirect("todolist")
    else:
        context = {"task_obj": task_obj}
        return render(request, "edit.html", context)


@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.delete()

    messages.error(
        request,
        (
            "Task -> {0} got deleted!".format(
                task.task,
            )
        ),
    )
    return redirect("todolist")


def index(request):
    context = {"index_text": "Welcome to Home page"}
    return render(request, "index.html", context)


def contact(request):
    context = {"contact_text": "Welcome to Contact us"}
    return render(request, "contact.html", context)


def about(request):
    context = {"about_text": "Welcome to About us"}
    return render(request, "about.html", context)
