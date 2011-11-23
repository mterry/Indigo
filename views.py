from django.shortcuts               import render_to_response, get_object_or_404, get_list_or_404
from django.http                    import HttpResponseRedirect
from django.template                import RequestContext
from django.contrib.auth.models     import User
from django.contrib.auth.forms      import UserCreationForm
from django.contrib                 import auth
from indigo.models                  import Project, Iteration, Task
from indigo.forms                   import CreateProjectForm, CreateIterationForm, CreateTaskForm, ModifyTaskForm
from django.core.context_processors import csrf
from datetime                       import date

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

  params = {'project': p, 'iteration': i, 'task': t}
  return render_base(request, params, 'task_detail.html')


# Project helpers
def all_projects():
  return Project.objects.all().order_by('name')

def projects_by_username(name):
  user = get_object_or_404(User, username=name)
  #return get_list_or_404(Project, collaborators=user).order_by('name')
  return Project.objects.filter(collaborators=user).order_by('name')


# Form processing views
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
        newUser.save();

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

def project_associate(request, project_id):
  if request.user.is_authenticated():
    p = get_object_or_404(Project, pk=project_id)

    if request.user not in p.get_collaborators():
      p.collaborators.add(request.user)
      p.save()

  return HttpResponseRedirect('/indigo/project/'+str(project_id)+'/');

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

def render_form(request, title, message, form_action, form, submit_text):
  params = {'title': title, 'message': message, 'form_action': form_action, 'form': form, 'submit_text': submit_text}
  params.update(csrf(request))
  return render_base(request, params, 'form.html')

def render_base(request, params, viewName):
  # Pass the RequestContext so we can get context in our templates for auth and media stuff
  return render_to_response(viewName, params, context_instance=RequestContext(request))
