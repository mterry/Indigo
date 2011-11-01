from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import Context, loader
from indigo.models import Project, Iteration, Task
from indigo.forms import CreateProjectForm

# Create your views here.
is_logged_in = False

def index(request):
  if is_logged_in:
    return projects_list(request)
  else:
    template = loader.get_template('index.html')
    context  = Context({
    })
	
  return HttpResponse(template.render(context))

def user_auth(request):
  return null

def projects_list(request, filter_type):
  if filter_type == 'all' or not is_logged_in:
    project_list = all_projects()

  elif filter_type == 'users' or is_logged_in:
    project_list = projects_by_username()

  return render_to_response('projects.html', {'project_list': project_list})


def projects_detail(request, project_id):
  return null

def iterations_list(request, project_id):
  return null

def iterations_detail(request, project_id, iteration_id):
  return null

def tasks_list(request, project_id, iteration_id):
  return null

def tasks_detail(request, project_id, iteration_id, task_id):
  return null

# Project responses

def all_projects():
  return Project.objects.all().order_by('name')

def projects_by_username(name):
  user = get_object_or_404(User, username=name)
  return get_list_or_404(Project, collaborators=user).order_by('name')

# Form processing views

def create_project(request):
  if request.method == 'POST':
    form = CreateProjectForm(request.POST)
    if form.is_valid():
      clean_data = form.cleaned_data
      project = Project(name=clean_data['name'],
        description=clean_data['description'],
        task_point_timescale=clean_data['task_point_timescale']
      )
      project.save()
      return HttpResponseRedirect('/projects/' + project.id + '/')

  else:
    form = CreateProjectForm()

  return render_to_response('create_project.html', {'form': form})

def create_iteration(request):
  if request.method == 'POST':
    form = CreateIterationForm(request.POST)
    if form.is_valid():
      clean_data = form.cleaned_data
      iteration = Iteration(name=clean_data['name'],
        number=clean_data['number']
      )
      iteration.save()
      # TODO: What is the path for this redirection? I.e. how do we redirect the
      # user to the newly created iteration?
      return HttpResponseRedirect('')

  else:
    form = CreateIterationForm()

  return render_to_response('create_iteration.html', {'form': form})
