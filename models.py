import datetime
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  velocity = models.IntegerField()
  task_point_timescale = models.PositiveIntegerField()
  collaborators = models.ManyToManyField(User, related_name='collaborators')
  owner = models.ForeignKey(User, related_name='owner')

  def __unicode__(self):
    return self.name

  def get_collaborators(self):
    pass

class Iteration(models.Model):
  name = models.CharField(max_length=50)
  number = models.PositiveIntegerField()
  velocity = models.IntegerField()
  project = models.ForeignKey(Project)
  due_date = models.DateField(null=False)
  finished = models.BooleanField(null=False)
  
  def __unicode__(self):
    return self.name

  def is_overdue(self):
    return (date.today > due_date)

  def is_finished(self):
    return finished

class Task(models.Model):
  name = models.CharField(max_length=50)
  number = models.PositiveIntegerField()
  description = models.TextField()
  points = models.PositiveIntegerField()
  assigned_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  iteration = models.ForeignKey(Iteration)
  closed = models.BooleanField(null=False)

  def __unicode__(self):
    return self.name

  def is_closed(self):
    return closed
