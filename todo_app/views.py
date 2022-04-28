from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, date, timedelta

from .forms import JoinForm, LoginForm, TaskForm

from django.contrib.auth.models import User
from .models import ToDoList
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

# function to print the welcome page
def home(request):

    if request.user.is_authenticated:
        return redirect('todo_app:dashboard')
    else:
        form = LoginForm(request.POST or None)

        error = ""

        if request.method == "POST":

            if form.is_valid():

                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('todo_app:dashboard')
                else:    
                    error = 'Invalid credentials'    
            else:
                error = 'Error validating the form'

        return render(request, 'todo_app/home.html', {"form": form, "error": error,})





# function to print the join page and traitement 
def join(request):

    form = JoinForm(request.POST or None)

    msg = ""

    if request.method == "POST":

        if form.is_valid():

            email = form.cleaned_data['email']
            user = User.objects.filter(email= email)

            if user.exists():
                msg = "This email has taken."
                #return render(request, 'todo_app/join.html', {"form": form, "failed": failed,})
            else:
                password = form.cleaned_data['password']
                user = User.objects.create_user(email, email, password)
                user.save()

                success = "Your account have been successfully created. Have a good experience."
                return render(request, 'todo_app/home.html', {"success": success,}) 

    return render(request, 'todo_app/join.html', {"form": form, "msg": msg,})



#function to access dahboard, login is required else redirect to login page
@login_required(login_url='/')
def dashboard(request):

    form = TaskForm(request.POST or None)
    person = User.objects.get(id = request.user.id)
    to_dos = ToDoList.objects.filter(user=person)

    if request.method == "POST":

        if form.is_valid():
            name = form.cleaned_data['name']
            todo = ToDoList()
            todo.name = name
            todo.user = person
            todo.status = "not done"
            todo.save()

            messages.add_message(request, messages.INFO, 'Todo added with success.')
            return redirect('todo_app:dashboard')

    return render(request, 'todo_app/dashboard.html', {'person': person, "to_dos": to_dos, "form": form} )




#function to delete specific to-do with id
@login_required(login_url='/')
def delete_todo(request, id):

    todo = ToDoList.objects.filter(id = id)

    todo.delete()
    
    messages.add_message(request, messages.INFO, 'Todo deleted with success.')

    return redirect('todo_app:dashboard')



#function to edit a specific to-do 
@login_required(login_url='/')
def edit_todo(request, id):

    todo = ToDoList.objects.filter(id = id)

    if request.POST['name'] != "":
        todo.update(name=request.POST['name'])
    
    messages.add_message(request, messages.INFO, 'Todo has successfully updated.')

    return redirect('todo_app:dashboard')



# function to complete to-do status. When to-do is complete, it's not possible to
#edit, delete, or change status of this to-do
@login_required(login_url='/')
def status_todo(request, id):

    todo = ToDoList.objects.filter(id = id)

    todo.update(status="done", completed_at = datetime.now() )
    
    messages.add_message(request, messages.INFO, 'Todo has successfully completed.')

    return redirect('todo_app:dashboard')



#function to filter all completed to-dos
@login_required(login_url='/')
def completed_todo(request):

    person = User.objects.get(id = request.user.id)
    to_dos = ToDoList.objects.filter(user=person, status="done")
    return render(request, 'todo_app/dashboard.html', {'person': person, "to_dos": to_dos} )
    #return redirect('todo_app:dashboard')



#function to filter all active to-dos
@login_required(login_url='/')
def active_todo(request):

    person = User.objects.get(id = request.user.id)
    to_dos = ToDoList.objects.filter(user=person, status="not done")
    return render(request, 'todo_app/dashboard.html', {'person': person, "to_dos": to_dos} )
    #return redirect('todo_app:dashboard')


"""@login_required(login_url='/')
def sorted_todo(request):

    person = User.objects.get(id = request.user.id)
    to_dos_all = ToDoList.objects.filter(user=person)

    to_dos_complete = ToDoList.objects.filter(user=person, status="done")

    to_dos_active = ToDoList.objects.filter(user=person, status="not done")
    if request.POST['start_date'] && request.POST['end_date']:

        start = request.POST['start_date']
        end = request.POST['end_date']
        to_dos_sorted = ToDoList.objects.filter(date__range=[start, end])
        return render(request, 'todo_app/analytics.html', {
            'person': person,
            "to_dos_all": to_dos_all,
            "to_dos_complete": to_dos_complete,
            "to_dos_active": to_dos_active,

        } )

    to_dos = ToDoList.objects.filter(user=person, status="not done")
    return render(request, 'todo_app/dashboard.html', {'person': person, "to_dos": to_dos} )
    #return redirect('todo_app:dashboard')
"""


# function to show analytics of their to-dos
@login_required(login_url='/')
def analytics_view(request):

    person = User.objects.get(id = request.user.id)
    to_dos_all = ToDoList.objects.filter(user=person)

    to_dos_sorted = ToDoList.objects.filter(user=person,
     completed_at__range=[datetime.now() - timedelta(days=7), datetime.now()], status="done")

    to_dos_complete = ToDoList.objects.filter(user=person, status="done")

    to_dos_active = ToDoList.objects.filter(user=person, status="not done")

    if request.method == "POST":

        if request.POST['start_date'] and request.POST['end_date']:

            start = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()

            end = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()

            to_dos_sorted = ToDoList.objects.filter(user=person,
             completed_at__range=[datetime.combine(start, datetime.min.time()),
              datetime.combine(end, datetime.min.time())],
             status="done")

            return render(request, 'todo_app/analytics.html', {
                'person': person,
                "to_dos_all": to_dos_all,
                "to_dos_complete": to_dos_complete,
                "to_dos_active": to_dos_active,
                "to_dos_sorted": to_dos_sorted

            } )


    return render(request, 'todo_app/analytics.html', {
        'person': person,
        "to_dos_all": to_dos_all,
        "to_dos_complete": to_dos_complete,
        "to_dos_active": to_dos_active,
        "to_dos_sorted": to_dos_sorted

    } )
    #return redirect('todo_app:dashboard')




#logout function
def logout_view(request):

    logout(request)
    messages.add_message(request, messages.INFO, 'Logout success!!!.')
    return redirect('/to-do-app/dashboard')