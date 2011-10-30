from django.db import models
from django.contrib.auth import models.User

class Project(models.Model):
  name = models.charField(max_length=50)
  description = models.textField()
  velocity = integerField()
  task_point_timescale = positiveIntegerField()
  collaborators = models.ManyToManyField(User)

  def __unicode__(self):
    return self.name

class Iteration(models.Model):
  name = models.charField(max_length=50)
  number = models.positiveIntegerField()
  velocity = models.integerField()
  project = models.ForeignKey(Project)
  
  def __unicode__(self):
    return self.name

class Task(models.Model):
  name = models.charField(max_length=50)
  description = models.textField()
  points = models.positiveIntegerField()
  assigned_to = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
  iteration = models.ForeignKey(Iteration)

  def __unicode__(self):
    return self.name
