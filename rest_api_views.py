from django.shortcuts               import render_to_response
from django.http                    import HttpResponse
from django.template                import RequestContext
from django.contrib.auth.models     import User
from django.contrib                 import auth
from indigo.models                  import Project, Iteration, Task, UserToken
from datetime                       import date
from django.views.decorators.csrf   import csrf_exempt
from django.template                import loader, Context

# All custom post requests need to be csrf exempt to prevent django throwing a fit
@csrf_exempt
def register(request):
  if request.method != 'POST':
    return HttpResponse(status=400)

  post = request.POST
  if 'user_name' not in post or 'password' not in post or post['user_name'] == '' or post['password'] == '':
    return HttpResponse(status=400)

  newUser = User.objects.create_user(post['user_name'], "", post['password'])
  newUser.is_active = True
  newUser.save()

  return HttpResponse(status=201)


@csrf_exempt
def authenticate(request, user_name):
  if request.method != 'POST':
    return HttpResponse(status=400)

  post = request.POST
  if 'password' not in post or post['password'] == '':
    return HttpResponse(status=400)

  user = User.objects.filter(username=user_name)
  if len(user) == 0:
    return HttpResponse(status=404)

  user = user[0]
  if user == None:
    return HttpResponse(status=404)

  if not user.check_password(post['password']):
    return HttpResponse(status=401)

  userToken = UserToken.objects.filter(user=user)
  if len(userToken) == 0:
    userToken = UserToken(user=user)
  else:
    userToken = userToken[0]

  userToken.generate_token()
  userToken.save()

  template = loader.get_template('rest_api/auth_token.xml')
  context = Context({'token': userToken.token, 'user_id': user.id})
  return HttpResponse(template.render(context), status=200, mimetype='text/xml')

@csrf_exempt
def invalidate(request, user_id):
  if request.method != 'POST':
    return HttpResponse(status=400)

  post = request.POST
  if 'token' not in post or post['token'] == '':
    return HttpResponse(status=400)

  user = User.objects.filter(id=user_id)
  if len(user) == 0:
    return HttpResponse(status=404)

  user = user[0]
  if user == None:
    return HttpResponse(status=404)

  userToken = UserToken.objects.filter(user=user)
  if len(userToken) == 0:
    return HttpResponse(status=401)
  else:
    userToken = userToken[0]

  if not userToken.token == post['token']:
    return HttpResponse(status=401)
  userToken.delete()

  return HttpResponse(status=204)

@csrf_exempt
def project_list(request, filter_type):
  if request.method != 'GET':
    return HttpResponse(status=400)

  if not filter_type == 'all' and not filter_type == 'user':
    return HttpResponse(status=400)

  get = request.GET
  if filter_type == 'user':
    if 'user_id' not in get or get['user_id'] == '':
      return HttpResponse(status=400)

    user = User.objects.filter(id=get['user_id'])
    if len(user) == 0:
      return HttpResponse(status=404)

    user = user[0]
    if user == None:
      return HttpResponse(status=404)

    projects = Project.objects.filter(collaborators=user)

  else:
    projects = Project.objects.all()

  template = loader.get_template('rest_api/project_list.xml')
  context = Context({'projects': projects})
  return HttpResponse(template.render(context), status=200, mimetype='text/xml')

@csrf_exempt
def project_detail(request, project_id):
  if request.method != 'GET':
    return HttpResponse(status=400)

  project = Project.objects.filter(id=project_id)
  if len(project) == 0:
    return HttpResponse(status=404)

  project = project[0]

  template = loader.get_template('rest_api/project_detail.xml')
  context = Context({'project': project})
  return HttpResponse(template.render(context), status=200, mimetype='text/xml')

@csrf_exempt
def iteration_list(request, project_id):
  if request.method != 'GET':
    return HttpResponse(status=400)

  project = Project.objects.filter(id=project_id)
  if len(project) == 0:
    return HttpResponse(status=404)

  project = project[0]

  iterations = Iteration.objects.filter(project=project)

  template = loader.get_template('rest_api/iteration_list.xml')
  context = Context({'iterations': iterations})
  return HttpResponse(template.render(context), status=200, mimetype='text/xml')

@csrf_exempt
def iteration_detail(request, iteration_id):
  if request.method != 'GET':
    return HttpResponse(status=400)

  iteration = Iteration.objects.filter(id=iteration_id)
  if len(iteration) == 0:
    return HttpResponse(status=404)

  iteration = iteration[0]

  template = loader.get_template('rest_api/iteration_detail.xml')
  context = Context({'iteration': iteration})
  return HttpResponse(template.render(context), status=200, mimetype='text/xml')

@csrf_exempt
def task_list(request, iteration_id):
  if request.method != 'GET':
    return HttpResponse(status=400)

  iteration = Iteration.objects.filter(id=iteration_id)
  if len(iteration) == 0:
    return HttpResponse(status=404)

  iteration = iteration[0]

  tasks = Task.objects.filter(iteration=iteration)

  template = loader.get_template('rest_api/task_list.xml')
  context = Context({'tasks': tasks})
  return HttpResponse(template.render(context), status=200, mimetype='text/xml')

@csrf_exempt
def task_detail(request, task_id):
  if request.method != 'GET':
    return HttpResponse(status=400)

  task = Task.objects.filter(id=task_id)
  if len(task) == 0:
    return HttpResponse(status=404)

  task = task[0]

  template = loader.get_template('rest_api/task_detail.xml')
  context = Context({'task': task})
  return HttpResponse(template.render(context), status=200, mimetype='text/xml')

@csrf_exempt
def task_create(request, iteration_id):
  if request.method != 'POST':
    return HttpResponse(status=400)

  # Verify that all the post params we need are here
  post = request.POST
  paramNames = ['user_id', 'token', 'task_name', 'task_description', 'task_points']
  if not verifyParams(paramNames, post):
    return HttpResponse(status=400)

  # Verify that this user has the right token and they can create a new task for this iteration
  user = User.objects.filter(id=post['user_id'])
  if len(user) == 0:
    return HttpResponse(status=404)
  user = user[0]

  userToken = UserToken.objects.filter(user=user)
  if len(userToken) == 0:
    return HttpResponse(status=401)
  userToken = userToken[0]

  if not userToken.token == post['token']:
    return HttpResponse(status=401)

  iteration = Iteration.objects.filter(id=iteration_id)
  if len(iteration) == 0:
    return HttpResponse(status=404)
  iteration = iteration[0]

  # Make sure this user can add a new task to this iteration
  if len(iteration.project.collaborators.filter(id=user.id)) == 0:
    return HttpResponse(status=401)

  newTask = Task(
    name=post['task_name'],
    number=iteration.next_task_number,
    description=post['task_description'],
    points=post['task_points'],
    iteration=iteration,
    closed=False
  )

  if 'assigned_to' in post and not post['assigned_to'] == None:
    assign_to = User.objects.filter(id=post['assigned_to'])
    if len(assign_to) == 0:
      return HttpResponse(status=404)

    newTask.assigned_to = assign_to[0]

  newTask.save()

  iteration.next_task_number += 1
  iteration.save()

  template = loader.get_template('rest_api/task_new.xml')
  context = Context({'task_id': newTask.id})
  return HttpResponse(template.render(context), status=201, mimetype='text/xml')

@csrf_exempt
def task_update(request, task_id):
  if request.method != 'POST':
    return HttpResponse(status=400)

  # Verify that all the post params we need are here
  post = request.POST
  paramNames = ['user_id', 'token', 'task_name', 'task_description', 'task_points', 'task_assigned_to', 'task_iteration', 'task_closed']
  if not verifyParams(paramNames, post):
    return HttpResponse(status=400)

  if not post['task_closed'] == 'True' and not post['task_closed'] == 'False':
    return HttpResponse(status=400)

  # Verify that this user has the right token and they can create a new task for this iteration
  user = User.objects.filter(id=post['user_id'])
  if len(user) == 0:
    return HttpResponse(status=404)
  user = user[0]

  userToken = UserToken.objects.filter(user=user)
  if len(userToken) == 0:
    return HttpResponse(status=401)
  userToken = userToken[0]

  if not userToken.token == post['token']:
    return HttpResponse(status=401)

  task = Task.objects.filter(id=task_id)
  if len(task) == 0:
    return HttpResponse(status=404)
  task = task[0]

  # Make sure this user can modify this task
  if len(task.iteration.project.collaborators.filter(id=user.id)) == 0:
    return HttpResponse(status=401)

  task.name = post['task_name']
  task.description = post['task_description']
  task.points = post['task_points']
  task.closed = post['task_closed'] == 'True'

  # Check for new iteration
  newIteration = Iteration.objects.filter(id=post['task_iteration'])
  if len(newIteration) == 0:
    return HttpResponse(status=404)
  newIteration = newIteration[0]

  if not newIteration.id == task.iteration.id:
    # Ensure the new iteration is in the same project
    if not newIteration.project.id == task.iteration.project.id:
      return HttpResponse(status=403)

    task.iteration = newIteration
    task.number = newIteration.next_task_number

    newIteration.next_task_number += 1
    newIteration.save()

  # Check for new assign to user
  if post['task_assigned_to'] == '-1':
    newAssignTo = None

  else:
    newAssignTo = User.objects.filter(id=post['task_assigned_to'])
    if len(newAssignTo) == 0:
      return HttpResponse(status=404)
    newAssignTo = newAssignTo[0]
  
  if not task.assigned_to == newAssignTo or not newAssignTo.id == task.assigned_to.id:
    # Ensure this new user is a collaborator of this project
    if not newAssignTo == None and len(task.iteration.project.collaborators.filter(id=newAssignTo.id)) == 0:
      return HttpResponse(status=403)

    task.assigned_to = newAssignTo

  task.save()

  return HttpResponse(status=204)

def verifyParams(paramNames, paramsDict):
  for param in paramNames:
    if param not in paramsDict or paramsDict[param] == None:
      return False

  return True
