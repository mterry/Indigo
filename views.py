from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.models import User
from indigo.models import Project, Iteration, Task
from indigo.forms import CreateProjectForm, CreateIterationForm, CreateTaskForm, ModifyTaskForm
from django.core.context_processors import csrf
from datetime import date

# Create your views here.

def index(request):
  if request.user.is_authenticated():
    return projects_list(request)
  else:
    template = loader.get_template('index.html')
    context  = Context({
    })
	
  return HttpResponse(template.render(context))

def registration(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/indigo/project/');

  else:
    return render_form(request,
                       'Registration',
                       'To Register enter your information below:',
                       '/indigo/registration/',
                       UserCreationForm(),
                       'Register!')

def project_list(request, filter_type):
  if filter_type == 'all' or not request.user.is_authenticated():
    project_list = all_projects()

  elif filter_type == 'users' or request.user.is_authenticated():
    project_list = projects_by_username(request.user.username)

  return render_to_response('projects.html', {'project_list': project_list})

def project_detail(request, project_id):
  p = get_object_or_404(Project, pk=project_id)
  iterations = Iteration.objects.filter(project=p)
  return render_to_response('project_detail.html', {'project': p, 'iterations': iterations})

def iteration_detail(request, project_id, iteration_id):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_id)
  return render_to_response('iteration_detail.html',
                            {'project': p, 'iteration': i})

def tasks_list(request, project_id, iteration_number):
  p = get_object_or_404(Project, pk=project_id)
  i = get_object_or_404(Iteration, project=p.id, number=iteration_number)
  task_list = get_list_or_404(Task, iteration=i)
  return render_to_response('task_list.html', {'task_list': task_list})

def task_detail(request, project_id, iteration_number, task_number):
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
  #return get_list_or_404(Project, collaborators=user).order_by('name')
  return Project.objects.filter(collaborators=user).order_by('name')

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
                          owner=request.user,
						              velocity=0,
                          next_iteration_number=0)
        project.save()

        user = User.objects.get(username=request.user.username)
        project.collaborators.add(user)
        project.save()
        return HttpResponseRedirect('/indigo/project/' + str(project.id) + '/')

  else:
    form = CreateProjectForm()

  return renderForm(request,
  					'Create Project:', 
  					'Create an project by filling in the form below!',
					'/indigo/project/add/',
					form,
					'Create!')

def create_iteration(request, project_id):
  if request.method == 'POST':
    project = get_object_or_404(Project, id=project_id)
    form = CreateIterationForm(request.POST)

    if request.user.is_authenticated() and \
       request.user.id in project.get_collaborators():

      if form.is_valid():
        clean_data = form.cleaned_data
        due_date = date(clean_data['year'], clean_data['month'], clean_data['day'])
        iteration = Iteration(name=clean_data['name'],
                              number=project.next_iteration_number,
                              velocity=0,
                              project=project,
                              due_date=due_date,
                              finished=False)
        iteration.save()

        project.next_iteration_number += 1
        project.save()

        # TODO: What is the path for this redirection? I.e. how do we redirect
        # the user to the newly created iteration?
        return HttpResponseRedirect('/indigo/project/' + str(project.id) + '/iteration/' +
                                    str(iteration.number) + '/')

  else:
    form = CreateIterationForm()

  return renderForm(request,
  					'Create Iteration:', 
  					'Create an iteration by filling in the form below!',
					'/indigo/project/' + str(project_id) + '/iteration/add/',
					form,
					'Create!')

def create_task(request, project_id, iteration_number):
  if request.method == 'POST':
    p = get_object_or_404(Project, id=project_id)
    i = get_object_or_404(Iteration, project=p, number=iteration_number)
    form = CreateTaskForm(request.POST, project=p)

    if request.user.is_authenticated() and \
       request.user.id in p.get_collaborators():

      if form.is_valid():
        clean_data = form.cleaned_data
        user_to_be_assigned = User.objects.get(id=clean_data['assigned_to'])
        task = task(name=clean_data['name'],
                    description=clean_data['description'],
                    points=clean_data['points'],
                    assigned_to=user_to_be_assigned,
                    iteration=i)
        task.save()

        # TODO: What is the path for this redirection? I.e. how do we redirect
        # the user to the newly created iteration?
        return HttpResponseRedirect('/projects/' + project.id + '/iteration/' +
                                    iteration.id + '/task/' + task.id + '/')

  else:
    form = CreateIterationForm()

  return render_to_response('create_iteration.html', {'form': form})

def modify_task(request, project_id, iteration_number, task_number):
  if request.method == 'POST':
    p = get_object_or_404(Project, id=project_id)
    i = get_object_or_404(Iteration, project=p, number=iteration_number)
    form = ModifyTaskForm(request.POST, project=p)

    if request.user.is_authenticated() and \
       request.user.id in p.get_collaborators():

      if form.is_valid():
        clean_data = form.cleaned_data
        user_to_be_assigned = User.objects.get(id=clean_data['assigned_to'])
        task = get_object_or_404(Task, iteration=i, number=task_number)
        task.description = clean_data['description']
        task.points = clean_data['points']
        task.assigned_to = user_to_be_assigned
        task.closed = clean_data['closed']
        task.save()

        # TODO: What is the path for this redirection? I.e. how do we redirect
        # the user to the newly created iteration?
        return HttpResponseRedirect('/projects/' + project.id + '/iteration/' +
                                    iteration.id + '/task/' + task.id + '/')

  else:
    form = CreateIterationForm()

  return renderForm('Create Task:', 
  					'Create an task by filling in the form below!',
					'/projects/' + project_id + '/iteration/' + iteration_number + '/task/' + task_number + '/')

def renderForm(request, title, message, form_action, form, submit_text):
	params = {'title': title, 'message': message, 'form_action': form_action, 'form': form, 'submit_text': submit_text}
	params.update(csrf(request))
	return render_to_response('form.html', params)
