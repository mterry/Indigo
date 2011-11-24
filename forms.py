from django import forms
from indigo.models import Project, Iteration
from django.contrib.auth.models import User
import datetime

class CreateProjectForm(forms.Form):
  name = forms.CharField(max_length=50, required=True)
  description = forms.CharField(required=True)
  task_point_timescale = forms.IntegerField(min_value=1, required=True)

class CreateIterationForm(forms.Form):
  name = forms.CharField(max_length=50, required=False)

  now = datetime.datetime.today()
  year = forms.IntegerField(min_value=now.year, required=True)
  month = forms.IntegerField(min_value=now.month, required=True)
  day = forms.IntegerField(min_value=now.day, required=True)

class CreateTaskForm(forms.Form):
  name = forms.CharField(max_length=50, required=True)
  description = forms.CharField(required=False)
  points = forms.IntegerField(min_value=1, required=True)
  assigned_to = forms.ChoiceField(choices = [])

  def __init__(self, project, data=None):
    super(CreateTaskForm, self).__init__(data)

    userChoices = [(-1, '')]
    for user_id in project.get_collaborators():
      user = User.objects.get(id=user_id)
      userChoices.append((user.id, user.username))
      
    self.fields['assigned_to'].choices = userChoices

class ModifyTaskForm(forms.Form):
  description = forms.CharField(required=False)
  points = forms.IntegerField(min_value=1, required=True)
  closed = forms.BooleanField(required=False)
  assigned_to = forms.ChoiceField(choices = [])

  def __init__(self, project, data=None):
    super(ModifyTaskForm, self).__init__(data)

    userChoices = [(-1, '')]
    for user_id in project.get_collaborators():
      user = User.objects.get(id=user_id)
      userChoices.append((user.id, user.username))

    self.fields['assigned_to'].choices = userChoices

class ModifyProjectForm(forms.Form):
  description = forms.CharField(required=True)
  task_point_timescale = forms.IntegerField(min_value=1, required=True)

class MoveTaskForm(forms.Form):
  other_iteration = forms.ChoiceField(choices = [])

  def __init__(self, project, iteration, data=None):
    super(MoveTaskForm, self).__init__(data)

    iteration_choices = [(-1, '')]
    for iteration in Iteration.objects.filter(project=project).exclude(pk=iteration.id):
      iteration_choices.append((iteration.number, iteration.name))

    self.fields['other_iteration'].choices = iteration_choices
