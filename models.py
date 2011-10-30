from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  velocity = models.IntegerField()
  task_point_timescale = models.PositiveIntegerField()
  collaborators = models.ManyToManyField(User)

  def __unicode__(self):
    return self.name

class Iteration(models.Model):
  name = models.CharField(max_length=50)
  number = models.PositiveIntegerField()
  velocity = models.IntegerField()
  project = models.ForeignKey(Project)
  
  def __unicode__(self):
    return self.name

class Task(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  points = models.PositiveIntegerField()
  assigned_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  iteration = models.ForeignKey(Iteration)

  def __unicode__(self):
    return self.name
