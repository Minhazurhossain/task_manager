from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model) :
    PENDING = "Pending"
    COMPLETED = "Completed"
    IN_PROGRESS ="In_Progress"
    STATUS = [
        (PENDING,"Pending"),
        (COMPLETED,"Completed"),
         (IN_PROGRESS," In_Progress")
    ]
    title = models.CharField(max_length=200, null=False, blank=False)
    discription = models.CharField(max_length=200, null=False, blank=False)
    category = models.CharField(max_length=200, default=None)
    due_date = models.DateTimeField(auto_now_add= True)
    status = models.CharField(max_length=200, choices=STATUS,default= PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

     
     
    def __str__(self):
        return self.title
