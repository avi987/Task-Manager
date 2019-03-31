from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=250)
    users = models.ManyToManyField(User)
    # createdBy = models.ForeignKey(User,related_name='created_by',on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('tasks:team_details',kwargs={'team_id':self.id})
    def __str__(self):
        return self.team_name

class Task(models.Model):
    Planned = "Planned"
    in_progress = "in_progress"
    done = "done"
    terminated = "terminated"
    status = ((Planned,"Planned"),(in_progress,'in_progress'),(done,'done'),(terminated,'terminated'))
    task_title = models.CharField(max_length=250)
    createdBy = models.ForeignKey(User,related_name='createdBy',on_delete=models.CASCADE)
    task_description = models.CharField(max_length=1000)
    task_assignee = models.ManyToManyField(User)
    task_status = models.CharField(max_length=30,choices=status,default=Planned)
    task_team = models.ForeignKey(Team,on_delete=models.CASCADE)

    def __str__(self):
        return self.task_title
    def get_absolute_url(self):
        return reverse('tasks:team_details',kwargs={'team_id':self.task_team.id})

class Comments(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    commentedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=5000)
    def __str__(self):
        return 'comments'
    def get_absolute_url(self):
        return reverse('tasks:task_details',kwargs={'team_id':self.task.task_team.id,'task_id':self.task.id})
