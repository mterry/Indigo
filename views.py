from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth import User
from indigo.models import Project, Iteration, Task
# Create your views here.

# View definitions
def user_auth(request):
  return null

def projects_list(request, username, name):
  return {
      'public': all_projects,
      'user_projects': projects_by_username(username)
    }[name](username)

def projects_detail(request, project_id):
  p = get_object_or_404(Project, pk=project_id)
  return render_to_response('indigo/project_detail.html', {'project': p})

def iterations_list(request, project_id):
  return render_to_response('indigo/iteration_list.html', {})

def iterations_detail(request, project_id, iteration_id):
  i = get_object_or_404(Iteration, pk=iteration_id)
  return render_to_response('indigo/iteration_detail.html', {'project_id': project_id, 'iteration_id': iteration_id)

def tasks_list(request, project_id, iteration_id):
  return render_to_response('indigo/task_list.html', {})

def tasks_detail(request, project_id, iteration_id, task_id):
  return render_to_response('indigo/task_detail.html', {})

# Project responses
def all_projects:
  project_list = Project.objects.all().order_by('name')
  return render_to_response('indigo/project_list.html', {'project_list': project_list})

def projects_by_username(name):
  user = User.objects.get(username=name)
  project_list = get_list_or_404(Project, collaborators=user).order_by('name')
  return render_to_response('indigo/project_list.html', {'project_list': project_list})
