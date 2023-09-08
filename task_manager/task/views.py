from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Task
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
import string
from django.urls import reverse
from django.core import serializers
# Create your views here.


def base(request):
    return render(request, 'base.html')

def index(request):
    return HttpResponse("this is the home page for task manager application")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task.html')  # redirect to home page or any other page
        else:
            message = "Invalid username or password"
            return render(request, 'base.html', {'message': message})
    else:
        return render(request, 'base.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')

def task(request):
  task_list = Task.objects.order_by('-creation_date')
  context = {'task_list': task_list}
  return render(request, 'task.html', context)


def add(request):
  if request.method == "POST":
    if(request.POST['detail'] != "" and request.POST['category'] != ""):
      task = Task(detail=request.POST['detail'], status=Task.PENDING, category=string.capwords(request.POST['category']))
      task.save()
      return HttpResponseRedirect(reverse('task'));

    messages.error(request, "Task Detail & Category can't be blank" )
  else:
    messages.error(request, "Wrong Method" )
  return HttpResponseRedirect(reverse('task'));

def delete(request):
  if request.method == "POST":
    post_body = json.loads(request.body)
    task = get_object_or_404(Task, pk=post_body.get("id"))
    task.delete()
    return JsonResponse({
        "success": "deleted"
    })

  return JsonResponse({
      "error": "Method Not Supported"
  })

def update(request):
  if request.method == "POST":
    post_body = json.loads(request.body)
    task = get_object_or_404(Task, pk=post_body.get("id"))
    task.status = Task.COMPLETE if post_body.get("status") == "True" else Task.INCOMPLETE
    task.save(update_fields=['status'])
    return JsonResponse({
        "success": "deleted"
    })

  return JsonResponse({
      "error": "Method Not Supported"
  })

def get_task(request):
  task_list = Task.objects.order_by('-creation_date')
  task_list_json = serializers.serialize('json', task_list)

  return HttpResponse(task_list_json, content_type="application/json")
