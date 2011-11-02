from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.models import User
from indigo.models import Project, Iteration, Task
from indigo.forms import CreateProjectForm

# Create your views here.

def index(request):
  if request.user.is_authenticated():
    return projects_list(request)
  else:
    template = loader.get_template('index.html')
    context  = Context({
    })
	
  return HttpResponse(template.render(context))

def projects_list(request, filter_type):
  if filter_type == 'all' or not request.user.is_authenticated():
    project_list = all_projects()

  elif filter_type == 'users' or request.user.is_authenticated():
    project_list = projects_by_username()

  return render_to_response('projects.html', {'project_list': project_list})

def projects_detail(request, project_id):
  p = get_object_or_404(Project, pk=project_id)
  return render_to_response('indigo/project_detail.html', {'project': p})

def iterations_list(request, project_id):
  p = get_object_or_404(Project, pk=project_d)
  iteration_list = get_list_or_404(Iteration, project=p)
  return render_to_response('iteration_list.html',
                            {'iteration_list': iteration_list})

def iterations_detail(request, project_id, iteration_id):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_number)
  return render_to_response('iteration_detail.html',
                            {'project': p, 'iteration': i})

def tasks_list(request, project_id, iteration_number):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_number)
  task_list = get_list_or_404(Task, iteration=i)
  return render_to_response('task_list.html', {'task_list': task_list})

def tasks_detail(request, project_id, iteration_number, task_number):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_number)
  t = get_object_or_404(Task, iteration=i.id, number=task_number)
  return render_to_response('task_detail.html', {'project': p,
                                                  'iteration': i,
                                                  'task': t})

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

    if request.user.is_authenticated():

      if form.is_valid():
        clean_data = form.cleaned_data
        project = Project(name=clean_data['name'],
                          description=clean_data['description'],
                          task_point_timescale=clean_data['task_point_timescale'],
                          owner=request.user)
        project.save()
        return HttpResponseRedirect('/projects/' + project.id + '/')

  else:
    form = CreateProjectForm()

  return render_to_response('create_project.html', {'form': form})

def create_iteration(request, project_id):
  if request.method == 'POST':
    form = CreateIterationForm(request.POST)

    if request.user.is_authenticated() and
       request.user.id in Project.objects.get(id=project_id):

      if form.is_valid():
        clean_data = form.cleaned_data
        iteration = Iteration(name=clean_data['name'],
                              number=clean_data['number'])
        iteration.save()

        # TODO: What is the path for this redirection? I.e. how do we redirect
        # the user to the newly created iteration?
        return HttpResponseRedirect('/projects/' + project.id + '/iteration/' +
                                    iteration.id + '/')

  else:
    form = CreateIterationForm()

  return render_to_response('create_iteration.html', {'form': form})

def create_task(request, project_id, iteration_id):
  if request.method == 'POST':
    form = CreateTaskForm(request.POST)

    if request.user.is_authenticated() and
       request.user.id in Project.objects.get(id=project_id):

      if form.is_valid():
        clean_data = form.cleaned_data
        user_to_be_assigned = User.objects.get(id=clean_data['assigned_to'])
        task = task(name=clean_data['name'],
                    description=clean_data['description'],
                    points=clean_data['points'],
                    assigned_to=user_to_be_assigned)
        task.save()

        # TODO: What is the path for this redirection? I.e. how do we redirect
        # the user to the newly created iteration?
        return HttpResponseRedirect('/projects/' + project.id + '/iteration/' +
                                    iteration.id + '/task/' task.id + '/')

  else:
    form = CreateIterationForm()

  return render_to_response('create_iteration.html', {'form': form})
