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
  name = forms.CharField(max_length=50, required=True)
  description = forms.CharField(required=False)
  points = forms.IntegerField(min_value=1, required=True)
  assigned_to = forms.ChoiceField(choices=Project.get_collaborators(), required=False)

class ModifyTaskForm(forms.Form):
  description = forms.CharField(required=False)
  points = forms.IntegerField(min_value=1, required=True)
  assigned_to = forms.ChoiceField(choices=Project.get_collaborators(), required=False)
  closed = forms.BooleanField(requird=False)
