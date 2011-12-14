from django.shortcuts               import render_to_response, get_object_or_404, get_list_or_404
from django.http                    import HttpResponseRedirect
from django.template                import RequestContext
from django.contrib.auth.models     import User
from django.contrib.auth.forms      import UserCreationForm
from django.contrib                 import auth
from indigo.models                  import Project, Iteration, Task
from indigo.forms                   import CreateProjectForm, CreateIterationForm, CreateTaskForm, ModifyTaskForm, ModifyProjectForm, MoveTaskForm
from django.core.context_processors import csrf
from datetime                       import date

import indigo.forms_view

# Content Pages
def index(request):
  if request.user.is_authenticated():
    return project_list(request)
  else:
    return render_base(request, {}, 'index.html')

def project_list(request, filter_type=''):
  if filter_type == 'all' or not request.user.is_authenticated():
    project_list = all_projects()

  elif filter_type == 'users' or request.user.is_authenticated():
    project_list = projects_by_username(request.user.username)

  return render_base(request, {'project_list': project_list}, 'projects.html')

def project_detail(request, project_id):
  p = get_object_or_404(Project, pk=project_id)
  iterations = Iteration.objects.filter(project=p)

  params = {'project': p, 'iterations': iterations}
  return render_base(request, params, 'project_detail.html')

def iteration_detail(request, project_id, iteration_number):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_number)
  tasks = Task.objects.filter(iteration=i)

  params = {'project': p, 'iteration': i, 'tasks': tasks}
  return render_base(request, params, 'iteration_detail.html')

def task_detail(request, project_id, iteration_number, task_number):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_number)
  t = get_object_or_404(Task, iteration=i.id, number=task_number)

  params = {'project': p, 'iteration': i, 'task': t, 'iteration_move_form': MoveTaskForm(p, i)}
  return render_base(request, params, 'task_detail.html')


# Project helpers
def all_projects():
  return Project.objects.all().order_by('name')

def projects_by_username(name):
  user = get_object_or_404(User, username=name)
  #return get_list_or_404(Project, collaborators=user).order_by('name')
  return Project.objects.filter(collaborators=user).order_by('name')

def render_base(request, params, templateName):
  # Pass the RequestContext so we can get context in our templates for auth and media stuff
  return render_to_response(templateName, params, context_instance=RequestContext(request))
