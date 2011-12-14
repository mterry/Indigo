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

import indigo.views

# This file contains views that show forms,
# and the code to process forms submissions
def registration(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)

    if form.is_valid():
      clean_data = form.cleaned_data

      if clean_data['password1'] == clean_data['password2']:
        newUser = User.objects.create_user(
                    clean_data['username'],
                    "",
                    clean_data['password1']
                  )
        newUser.is_active = True
        newUser.save()

        return HttpResponseRedirect('/indigo/login/')
      else:
        return HttpResponseRedirect('/indigo/registration/')

  if request.user.is_authenticated():
    return HttpResponseRedirect('/indigo/project/');

  else:
    return render_form(request,
                       'Registration',
                       'To Register enter your information below:',
                       '/indigo/registration/',
                       UserCreationForm(),
                       'Register!')


# Projects form processing
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
        return HttpResponseRedirect('/indigo/')

    # Not autheticated redirect to login 
    else:
      return HttpResponseRedirect('/indigo/login/')
  
  form = CreateProjectForm()
  return render_form(request, 'Create Project:', 
  					         'Create an project by filling in the form below!',
					           '/indigo/project/add/', form, 'Create!')

def modify_project(request, project_id):
  p = get_object_or_404(Project, id=project_id)
  if request.method == 'POST':
    form = ModifyProjectForm(request.POST)

    if request.user.is_authenticated() and \
       request.user.id in p.get_collaborators():

      if form.is_valid():
        clean_data = form.cleaned_data
        p.description = clean_data['description']
        p.task_point_timescale = clean_data['task_point_timescale']
        p.save()
        return HttpResponseRedirect('/indigo/project/'+str(p.id)+'/')

      else:
        return HttpResponseRedirect('/indigo/project/'+str(p.id)+'/modify/')

    # Not autheticated redirect to login 
    else:
      return HttpResponseRedirect('/indigo/login/')


  form = ModifyProjectForm()
  return render_form(request, 'Modify Project:', 'Modify a project by filling in the form below!',
					           '/indigo/project/'+str(project_id)+'/edit/',
                     form, 'Update!')

def project_associate(request, project_id):
  if request.user.is_authenticated():
    p = get_object_or_404(Project, pk=project_id)

    if request.user not in p.get_collaborators():
      p.collaborators.add(request.user)
      p.save()

  return HttpResponseRedirect('/indigo/project/'+str(project_id)+'/');

# Iteration form processing
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
                              finished=False,
                              next_task_number=0)
        iteration.save()

        project.next_iteration_number += 1
        project.save()

        return HttpResponseRedirect('/indigo/project/' + str(project.id) + '/iteration/' + str(iteration.number) + '/')

      else:
        return HttpResponseRedirect('/indigo/')

    # Not autheticated redirect to login 
    else:
      return HttpResponseRedirect('/indigo/login/')

  form = CreateIterationForm()
  return render_form(request, 'Create Iteration:', 
                     'Create an iteration by filling in the form below!',
					           '/indigo/project/' + str(project_id) + '/iteration/add/',
					           form, 'Create!')

# Task form processing
def create_task(request, project_id, iteration_number):
  if request.method == 'POST':
    p = get_object_or_404(Project, id=project_id)
    i = get_object_or_404(Iteration, project=p, number=iteration_number)
    form = CreateTaskForm(p, request.POST)

    if request.user.is_authenticated() and \
       request.user.id in p.get_collaborators():

      if form.is_valid():
        clean_data = form.cleaned_data
        if clean_data['assigned_to'] != '-1':
          user_to_be_assigned = User.objects.get(id=clean_data['assigned_to'])
        else:
          user_to_be_assigned = None
        task = Task(name=clean_data['name'],
                    number=i.next_task_number,
                    description=clean_data['description'],
                    points=clean_data['points'],
                    assigned_to=user_to_be_assigned,
                    iteration=i)
        task.save()

        i.next_task_number += 1
        i.save()

        # Redirect to iteration detail screen
        return HttpResponseRedirect('/indigo/project/' + str(p.id) + '/iteration/' + str(i.number) + '/')

      else:
        return HttpResponseRedirect('/indigo/')

    # Not autheticated redirect to login 
    else:
      return HttpResponseRedirect('/indigo/login/')

  p = get_object_or_404(Project, id=project_id)
  form = CreateTaskForm(p)
  return render_form(request, 'Create Task:', 'Create a task by filling in the form below!',
				             '/indigo/project/' + str(project_id) + '/iteration/' + str(iteration_number) + '/task/add/',
				             form, 'Create!')

def modify_task(request, project_id, iteration_number, task_number):
  p = get_object_or_404(Project, id=project_id)
  if request.method == 'POST':
    i = get_object_or_404(Iteration, project=p, number=iteration_number)
    form = ModifyTaskForm(p, request.POST)

    if request.user.is_authenticated() and \
       request.user.id in p.get_collaborators():

      if form.is_valid():
        clean_data = form.cleaned_data
        task = get_object_or_404(Task, iteration=i, number=task_number)
        task.description = clean_data['description']
        task.points = clean_data['points']
        task.closed = clean_data['closed']
  
        if clean_data['assigned_to'] == '-1':
          task.assigned_to = None
        else:
          task.assigned_to = User.objects.get(id=clean_data['assigned_to'])
        task.save()

        return HttpResponseRedirect('/indigo/project/' + str(p.id) + '/iteration/' + str(i.number) + '/task/' + str(task.number) + '/')

      else:
        return HttpResponseRedirect('/indigo/')

    # Not autheticated redirect to login 
    else:
      return HttpResponseRedirect('/indigo/login/')


  form = ModifyTaskForm(p)
  return render_form(request, 'Modify Task:', 'Modify a task by filling in the form below!',
					           '/indigo/project/'+str(project_id)+'/iteration/'+str(iteration_number)+'/task/'+str(task_number)+'/edit/',
                     form, 'Update!')

def move_task(request, project_id, iteration_number, task_number):
  if request.method == 'POST' and request.user.is_authenticated():
    project = get_object_or_404(Project, pk=project_id)
    iteration = get_object_or_404(Iteration, number=iteration_number)
    task = get_object_or_404(Task, number=task_number)

    form = MoveTaskForm(project, iteration, request.POST)
    if form.is_valid():
      clean_data = form.cleaned_data

      if clean_data['other_iteration'] != '-1':
        task.iteration = Iteration.objects.get(number=clean_data['other_iteration'])
        task.save()
        iteration_number = clean_data['other_iteration']

    else:
      return HttpResponseRedirect('/indigo/')

  return HttpResponseRedirect('/indigo/project/'+str(project_id)+'/iteration/'+str(iteration_number)+'/task/'+str(task_number)+'/')

def render_form(request, title, message, form_action, form, submit_text):
  params = {'title': title, 'message': message, 'form_action': form_action, 'form': form, 'submit_text': submit_text}
  params.update(csrf(request))
  return indigo.views.render_base(request, params, 'form.html')
