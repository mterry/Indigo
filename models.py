from datetime import date
from django.db import models
from django.contrib.auth.models import User
import random

class Project(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField()
  velocity = models.IntegerField()
  task_point_timescale = models.PositiveIntegerField()
  collaborators = models.ManyToManyField(User, related_name='collaborators')
  owner = models.ForeignKey(User, related_name='owner')
  next_iteration_number = models.IntegerField()

  def __unicode__(self):
    return self.name

  def get_collaborators(self):
    collaborator_dict = dict()
    collaborator_list = self.collaborators.all()
    for collaborator in collaborator_list:
      collaborator_dict[collaborator.id] = collaborator.username
    
    return collaborator_dict

class Iteration(models.Model):
  name = models.CharField(max_length=50)
  number = models.PositiveIntegerField()
  velocity = models.IntegerField()
  project = models.ForeignKey(Project)
  due_date = models.DateField(null=False)
  finished = models.BooleanField(null=False)
  next_task_number = models.IntegerField()
  
  def __unicode__(self):
    return self.name

  def is_overdue(self):
    return (date.today() > due_date)

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

class UserToken(models.Model):
  user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
  token = models.CharField(max_length=20)

  def generate_token(self):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

    # Length of character list
    chars_length = len(chars) - 1

    random.seed()

		# Start our string
    newToken = chars[random.randint(0, chars_length)]
	   
		# Generate random string
    i = 1
    while not i == 20:
      #Grab a random character from our list
			c = chars[random.randint(0, chars_length)]
		   
			# Make sure the same two characters don't appear next to each other
			if not c == newToken[i - 1]:
				newToken += c
				i += 1

    self.token = newToken
