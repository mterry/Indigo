from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import Context, loader
from indigo.models import Project, Iteration, Task

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
		project_list = projects_by_user()

  	return render_to_response('projects.html', {'project_list': project_list})

def create_project(request, name):
	project = Project(name=name, description='', velocity=0, task_point_timescale=1)
	project.save()
	return HttpResponse('Worked!');

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
  return get_list_or_404(Project, collaborators=user.id).order_by('name')
