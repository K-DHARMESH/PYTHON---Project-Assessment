"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('task/', views.task, name='task'),
    path('mytask/', views.mytask, name='mytask'),
    path('task/complate/<int:task_id>/', views.taskcomplate, name='taskcomplate'),
    path('task/delete/<int:task_id>/', views.taskdelete, name='taskdelete'),
    path('task/edit/<int:task_id>/', views.taskedit, name='taskedit'),
    path('admindash/', views.admindash, name='admindash'),
    path('all-tasks/', views.all_tasks, name='all_tasks'),
    path('team_tasks/', views.team_tasks, name='team_tasks'),
    path('adminpanel/', views.adminpanel, name='adminpanel'),


   
]
