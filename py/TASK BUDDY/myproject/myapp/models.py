from ast import mod
import profile
from turtle import mode
from django.db import models

# Create your models here.


class User(models.Model):
    
    name = models.CharField( max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    profile = models.ImageField(default="", upload_to="profile/")
    selection = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('User', 'User')], default="User")
    
    def __str__(self):
        return f"{self.name}"
    
    
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=[("High","High"),("Medium","Medium"),("Low","Low")])
    status = models.CharField(max_length=20, choices=[("Pending","Pending"),("In Progress","In Progress"),("Completed","Completed")], default="Pending")
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="tasks")

    def __str__(self):
        return self.title

