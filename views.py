from django.http import HttpResponse
from django.template import Context, loader
# Create your views here.

def index(request):
	template = loader.get_template('index.html')
	context  = Context({
		'message': 'Hello there stranger!',
	})
	return HttpResponse(template.render(context))

def user_auth(request):
  return null

def projects_list(request, username):
  return null

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


