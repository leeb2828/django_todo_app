from django.shortcuts import render, redirect 
from todo_app.models import TodoList, Task 
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_protect
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User 
#
from django.contrib.auth import authenticate, login, logout  
from django.contrib.auth.decorators import login_required

"""
Fetch all Todo Lists from the database.
Returns a list.
"""
def get_all_list_names():
    todoLists = TodoList.objects.all()
    todoLists = list(todoLists)

    list_names = [] 
    for item in todoLists:
        list_names.append(item.name)

    return list_names 



"""
Fetch all Tasks from the database (using the 
todo list names from the parameter).
Returns a list of lists.
"""
def get_all_tasks(list_names):
    all_tasks = []
    
    for i in list_names:
        identified_list = TodoList.objects.get(name=i)
        task_objs = Task.objects.filter(todolist_id=identified_list)
        task_objs = list(task_objs)
        names_only = []
        for item in task_objs:
            name = item.name
            names_only.append(name)

        all_tasks.append(names_only)

    return all_tasks 



def delete_list(list_name):
    todo_list = TodoList.objects.get(name=list_name)
    todo_list.delete()



def delete_completed_tasks(request):
    tasks_to_delete = [] 
    index = 2
    for key, value in request.POST.items():
        if index <= 0:
            tasks_to_delete.append(key)
        index = index - 1
    
    for task in tasks_to_delete:
        t = Task.objects.get(name=task)
        t.delete()



"""
Create a dictionary storing all of the todo lists and 
their tasks (as list values). Returns the dictionary.
"""
def create_everything(list_names, task_groups):
    everything = {}
    for i in range(0, len(list_names)):
        key = list_names[i]
        values = task_groups[i]
        everything[key] = values 

    return everything



def add_new_list(request):
    new_todo_list = request.POST.get('addNewList')
    if (len(new_todo_list) < 1):
        new_todo_list = "None"
    elif (len(new_todo_list) > 18):
        new_todo_list = new_todo_list[:18]
    query = TodoList(name=new_todo_list)
    query.save()



def add_new_task(request, list_name):
    new_task = request.POST.get('addNewTask')
    if (len(new_task) < 1):
        new_task = "None"
    elif (len(new_task) > 22):
        new_task = new_task[:22]

    todo_list_name = TodoList.objects.get(name=list_name)
    query = Task(name=new_task, todolist_id=todo_list_name)
    query.save() 


# ROUTING (see urls.py)
"""
Get username and password from the signup form.
If the user doesn't already exist, create new user
using data from the form.
"""
def signup_user(request):
    username = request.POST['name']
    password = request.POST['password']

    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password=password)
        user.save()
    
    return redirect('login')


# ROUTING (see urls.py)
def login_user(request):
    username = request.POST['name']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password) 
    if user is not None:
        login(request, user)
        return redirect("index")
    else:
        return HttpResponse("Invalid Credentials")


# ROUTING (see urls.py)
""" delete the session data that was associated with the logged in user."""
def logout_user(request):
    logout(request)
    return redirect('login')
        

# ROUTING (see urls.py)
def login_page(request):
    form1 = LoginForm()
    form2 = SignUpForm()
    context = {'loginform': form1, 'signupform': form2}
    return render(request, 'registration/login.html', context)


    
# ROUTING (see urls.py)
""" 
This method either 
- Creates a new todo list
- Add a new task to a list 
"""
def add_stuff(request, list_name):
    if request.method == 'POST':
        if 'addNewTask' in request.POST: 
            add_new_task(request, list_name)
            return redirect('home', name=list_name)
        elif 'addNewList' in request.POST:
            add_new_list(request)
            return redirect('index')
    
    elif request.method == 'GET':
        return redirect('index')



# ROUTING (see urls.py)
"""
This method is called when the user selects the 
option to either delete a list or a task/tasks
from a list.
"""
def delete_stuff(request, list_name):
    if request.method == 'POST':
        if 'list' in request.POST:
            delete_list(list_name)
            return redirect('index')
        elif 'tasks' in request.POST:
            delete_completed_tasks(request)
            return redirect('home', name=list_name)
    
    return redirect('index')



# ROUTING (see urls.py)
"""
Fetch all of the todo lists and tasks from the database. 
NOTE: Only the list of Todo Lists, The first list name, and the 
tasks for the first list are displayed on the page.
If the user has not created any todo lists 
yet, only the "todo list" title and the option to create a new
list will appear on the page.
"""
@login_required 
def index(request):
    # A list of todo lists (displayed on the page)
    list_names = get_all_list_names() 
    task_groups = get_all_tasks(list_names) # a list of lists
    everything = create_everything(list_names, task_groups)
    if list(everything.keys()):
        # A string (displayed on the page)
        displayed_list = list(everything.keys())[0]
        # a list (displayed on the page)
        displayed_tasks = list(everything.values())[0]
    else:
        list_names = None 
        displayed_list = None
        displayed_tasks = None 
    
    _all = {"names": list_names, "first_list": displayed_list, "first_tasks": displayed_tasks}
    return render(request, 'todo_app/index.html', _all)



# ROUTING (see urls.py)
""" 
Fetch all of the todo lists and tasks from the database.
Using the "name" variable from the parameter, the correct
list and the tasks associated with that list, get displayed 
on the page. This method gets called when a user selects a 
specific todo list from the page.
"""
@login_required
def home(request, name):
    list_names = get_all_list_names()
    task_groups = get_all_tasks(list_names) 
    everything = create_everything(list_names, task_groups)

    displayed_list = name 
    displayed_tasks = list(everything[name])

    _all = {"names": list_names, "first_list": displayed_list, "first_tasks": displayed_tasks}
    return render(request, 'todo_app/index.html', _all)

