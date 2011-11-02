from django import forms
from indigo.models import Project

class CreateProjectForm(forms.Form):
  subject = forms.CharField(max_length=50, required=True)
  description = forms.CharField(required=True)
  task_point_timescale = forms.IntegerField(min_value=1, required=True)

class CreateIterationForm(forms.Form):
  name = forms.CharField(max_length=50, required=False)
  number = forms.IntegerField(min_value=1, required=True)

class CreateTaskForm(forms.Form):
  def __init__(self, project):
    self.project = project

  name = forms.CharField(max_length=50, required=True)
  description = forms.CharField(required=False)
  points = forms.IntegerField(min_value=1, required=True)
  assigned_to = forms.ChoiceField(choices=self.project.get_collaborators(), required=False)

class ModifyTaskForm(forms.Form):
  def __init__(self, project):
    self.project = project

  description = forms.CharField(required=False)
  points = forms.IntegerField(min_value=1, required=True)
  assigned_to = forms.ChoiceField(choices=self.project.get_collaborators(), required=False)
  closed = forms.BooleanField(requird=False)
