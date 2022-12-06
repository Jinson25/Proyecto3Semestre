from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
# Create your views here.

# Inicio
def home(request):
    return render(request, 'home.html')
# Crear Usuarios
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registar usuarios
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "User ya existe"
                })
    return render(request, 'signup.html', {
        'form': UserCreationForm,
        'error': "Contraseña no coincide"
    })
# vista Tareas
def tasks(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'tasks.html',{'tasks': tasks})
#crear Tareas
def createTask(request):
    if request.method == 'GET':
        return render(request, 'create.html',{
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            newTask = form.save(commit=False)
            newTask.user = request.user
            newTask.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create.html', {
                'form': TaskForm,
                'error': 'Proporciana datos validos'
            })
#Tareas detalle
def detailTask(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render (request, 'taskDetails.html',{'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, intance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render (request, 'taskDetails.html',{'task': task, 'form': form,
                                                        'error': "Error al actualizar tarea"})
#Tarea completado
def completeTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.dateCompleted = timezone.now()
        task.save()
        return redirect('tasks')
#tarea Eliminar
def deleteTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
# cerrar Session
def signout(request):
    logout(request)
    return redirect('home')
# Iniciar Session
def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña es incorrecta'
            }) 
        else:
            login(request, user)
            return redirect('tasks')
