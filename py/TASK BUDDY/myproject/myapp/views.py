from os import sep
from django.shortcuts import render, redirect
from .models import User
from .models import Task
from django.utils.timezone import now
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    
    if user.selection == "Admin":
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=user)


    overdue_tasks = tasks.filter(due_date__lt=now().date(), status="Pending")
    for task in overdue_tasks:
        send_mail(
            subject="Task Overdue Reminder",
            message=f"Hello {user.name},\n\nYour task '{task.title}' is overdue!\nDue Date was: {task.due_date}\n\n- TaskBuddy",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        
    pending = tasks.filter(status="Pending").count()
    completed = tasks.filter(status="Completed").count()
    overdue = tasks.filter(due_date__lt=now().date()).exclude(status="Completed").count()
    assigned = tasks.count()

    context = {
        'myuser': user,
        'tasks': tasks,
        'pending': pending,
        'completed': completed,
        'overdue': overdue,
        'assigned': assigned,
    }
    return render(request, 'index.html', context)


def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['user_id'] = user.id
                request.session['profile'] = user.profile.url
                request.session['selection'] = user.selection
                msg = "login suceesfully !!"
                
                if user.selection.lower() == "admin":
                    return redirect('admindash')
                else:
                    return redirect('index')
            
            else:
                msg = "password does not match !!"
                return render(request, 'login.html', {'msg':msg})
            
        except User.DoesNotExist:
            msg = "Email does not match !!"
            return render(request, 'login.html', {'msg':msg})
    else:    
        return render(request, 'login.html')
    
    

def signup(request):
    if request.method == "POST":
        try:
            
            user = User.objects.get(email=request.POST['email'])
            
            msg = "Email Alorady Exits !!"
            return render(request, 'signup.html', {"msg":msg})
        
        except User.DoesNotExist:
            if request.POST['password'] == request.POST['cpassword']:
        
                user = User.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    profile = request.FILES['profile'],
                    selection = request.POST['selection']
                )
                
                msg = "signup succesfully please login !!"
                return redirect('login')
            else:
                msg = "password and confirm password does not match !!"
                return render(request, 'signup.html', {'msg':msg})
    else:
        return render(request, 'signup.html')
    
    

def logout(request):
    request.session.pop('email',None)
    request.session.pop('user_id',None)
    request.session.pop('selection',None)
    return redirect('login')


def profile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return render(request, 'login.html')
    
    user = User.objects.get(id=user_id)
    
    if request.method == "POST":
        
        
        user.name = request.POST.get('name',user.name)
        
        if 'profile' in request.FILES:
            user.profile = request.FILES['profile']
            
        user.save()
        
        request.session['profile'] = user.profile.url
        
        msg = "profile Updated !!"
        return render(request, 'index.html', {'msg':msg , 'myuser':user})
           
    else:
        return render(request, 'profile.html', {'myuser':user})
    
    
    
def task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        status = request.POST.get("status")
        due_date = request.POST.get("due_date")
        assigned_to_id = request.POST.get("assigned_to")

        assigned_to = User.objects.get(id=assigned_to_id) if assigned_to_id else None

        Task.objects.create(
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date,
            assigned_to=assigned_to
        )
        
        send_mail(
            subject="New Task Assigned",
            message=f"Hello {assigned_to.name},\n\n"
                    f"You have been assigned a new task: {title}\n"
                    f"Due Date: {due_date}\n\n"
                    "Please check your dashboard.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[assigned_to.email],
            fail_silently=False,
        )
        
        return redirect("index")

    team_members = User.objects.all()
    return render(request, "task.html", {"team_members": team_members})

    
def mytask(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    tasks = Task.objects.filter(assigned_to=user).order_by('due_date')

    return render(request, 'mytask.html', {'tasks': tasks, 'myuser': user})



def taskcomplate(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = "Completed"
    task.save()
    return redirect('mytask')


def taskdelete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('mytask')


def taskedit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.title = request.POST.get('title')
        task.priority = request.POST.get('priority')
        task.due_date = request.POST.get('due_date')
        task.save()
        send_mail(
            subject="Task Updated",
            message=f"Hello {task.assigned_to.name},\n\nYour task has been updated.\n\nTitle: {task.title}\nStatus: {task.status}\nDue Date: {task.due_date}\n\n- TaskBuddy",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[task.assigned_to.email], 
            fail_silently=False,
        )
        return redirect('mytask')

    return render(request, 'taskedit.html', {'task': task})


def admindash(request):
    if request.session.get('selection') != "admin":
        return redirect('login')

    total_users = User.objects.count()
    total_tasks = Task.objects.count()
    pending = Task.objects.filter(status="Pending").count()
    completed = Task.objects.filter(status="Completed").count()
    overdue = Task.objects.filter(due_date__lt=now().date()).exclude(status="Completed").count()
    
    users = User.objects.all()
    tasks = Task.objects.all()


    context = {
        'total_users': total_users,
        'total_tasks': total_tasks,
        'pending': pending,
        'completed': completed,
        'overdue': overdue,
        'users': users,
        'tasks': tasks,
    }
    return render(request, 'admindash.html', context)


def all_tasks(request):
    user_id = request.session.get('user_id')
    if not user_id or request.session.get('selection') != "admin":
        return redirect('login')   # 

    tasks = Task.objects.all().select_related('assigned_to')  # सभी users के tasks
    return render(request, 'all_tasks.html', {'tasks': tasks})


def team_tasks(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    current_user = User.objects.get(id=user_id)
    # बाकी users के tasks fetch करना
    tasks = Task.objects.exclude(assigned_to=current_user)

    context = {
        'myuser': current_user,
        'tasks': tasks,
    }
    return render(request, 'team_tasks.html', context)



def adminpanel(request): 
    if request.session.get('selection') != "admin":
        return redirect('login')

    tasks = Task.objects.all()
    
    return render(request, 'adminpanel.html', {'tasks':tasks})
    