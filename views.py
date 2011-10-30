from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth import User
from indigo.models import Project, Iteration, Task

# View definitions

# The function user_auth is a switch-case function: it takes an argument 'name'
#   defined in urls.py and selects and runs the function specified by the 'name'
#   argument. It then returns the selected function's returned HttpResponse (created
#   by render_to_response) to the specified template.
def user_auth(request, name):
  return {
      'login': login,
      'logout': logout,
      'create_user': create_user
    }[name]()

# The function projects_list is a switch-case function: it takes an argument 'name'
#   defined in urls.py and selects and runs the function specified by the 'name'
#   argument. It then returns the selected function's returned HttpResponse (created
#   by render_to_response) to the specified template.
def projects_list(request, username, name):
  return {
      'public': all_projects,
      'user_projects': projects_by_username(username)
    }[name](username)

def projects_detail(request, project_id):
  p = get_object_or_404(Project, pk=project_id)
  return render_to_response('indigo/project_detail.html', {'project': p})

def iterations_list(request, project_id):
  p = get_object_or_404(Project, pk=project_id)
  iteration_list = get_list_or_404(Iteration, project=p.id)
  return render_to_response('indigo/iteration_list.html', {'iteration_list': iteration_list})

def iterations_detail(request, project_id, iteration_number):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_number)
  return render_to_response('indigo/iteration_detail.html', {'project': p, 'iteration': i})

def tasks_list(request, project_id, iteration_number):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_number)
  task_list = get_list_or_404(Task, iteration=i.id)
  return render_to_response('indigo/task_list.html', {'task_list': task_list})

def tasks_detail(request, project_id, iteration_number, task_number):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_number)
  t = get_object_or_404(Task, iteration=i.id, number=task_number)
  return render_to_response('indigo/task_detail.html', {'project': p, 'iteration': i, 'task': t})


# User auth responses

# TODO: Eliminate this view response function and replace it with a template call
#   in urls.py
# This response function passes the necessary data to the login.html template
def login:
  return render_to_response('indigo/login.html', {})

# TODO: Eliminate this view response function and replace it with a template call
#   in urls.py
# This response function passes the necessary data to the logout.html template
def logout:
  return render_to_response('indigo/logout.html', {})

# TODO: Eliminate this view response function and replace it with a template call
#   in urls.py
# This response function passes the necessary data to the create_user.html template
def create_user:
  return render_to_response('indigo/create_user.html', {})

# Project responses

def all_projects:
  project_list = Project.objects.all().order_by('name')
  return render_to_response('indigo/project_list.html', {'project_list': project_list})

def projects_by_username(name):
  user = get_object_or_404(User, username=name)
  project_list = get_list_or_404(Project, collaborators=user.id).order_by('name')
  return render_to_response('indigo/project_list.html', {'project_list': project_list})
