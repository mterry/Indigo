from django.conf.urls.defaults import patterns, include, url


# Url matching patterns for our task pages and form submissions
task_patterns = patterns('',
	url(r'^(?P<task_number>\d+)/$', 'indigo.views.task_detail'),
	url(r'^add/$', 'indigo.forms_view.create_task'),
	url(r'^(?P<task_number>\d+)/edit/$', 'indigo.forms_view.modify_task'),
	url(r'^(?P<task_number>\d+)/move/$', 'indigo.forms_view.move_task'),
)

# Url matching patterns for our iteration pages and form submissions
iteration_patterns = patterns('',
	url(r'^(?P<iteration_number>\d+)/task/', include(task_patterns)),

	url(r'^(?P<iteration_number>\d+)/$', 'indigo.views.iteration_detail'),
	url(r'^add/$', 'indigo.forms_view.create_iteration'),
)

# Url matching patterns for our project pages and form submissions
project_patterns = patterns('',
	url(r'^(?P<project_id>\d+)/iteration/', include(iteration_patterns)),

	url(r'^(?P<project_id>\d+)/$', 'indigo.views.project_detail'),
	url(r'^(?P<project_id>\d+)/edit/$', 'indigo.forms_view.modify_project'),
	url(r'^add/$', 'indigo.forms_view.create_project'),

  url(r'^$', 'indigo.views.project_list'),
	url(r'^(?P<filter_type>\w*)/$', 'indigo.views.project_list'),
	url(r'^(?P<project_id>\d+)/associate/$', 'indigo.forms_view.project_associate'),
)

# Url matching patterns for our restful api calls
api_patterns = patterns('indigo.rest_api_views',
	url(r'^register/$', 'register'),
	url(r'^authenticate/(?P<user_name>\w+)/$', 'authenticate'),
	url(r'^invalidate/(?P<user_id>\d+)/$', 'invalidate'),
	url(r'^project/list/(?P<filter_type>\w*)/$', 'project_list'),
	url(r'^project/(?P<project_id>\d*)/$', 'project_detail'),
	url(r'^iteration/list/(?P<project_id>\w*)/$', 'iteration_list'),
	url(r'^iteration/(?P<iteration_id>\d*)/$', 'iteration_detail'),
	url(r'^task/list/(?P<iteration_id>\w*)/$', 'task_list'),
	url(r'^task/(?P<task_id>\d*)/$', 'task_detail'),
	url(r'^task/create/(?P<iteration_id>\w*)/$', 'task_create'),
	url(r'^task/update/(?P<task_id>\w*)/$', 'task_update'),
)

# Url matching patterns for our basic auth pages and the entry into our project/iteration/tasks and api patterns
urlpatterns = patterns('',
	url(r'^$', 'indigo.views.index'),
	url(r'^registration/$', 'indigo.forms_view.registration'),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/indigo/'}),

	url(r'^project/', include(project_patterns)),

	url(r'^api/', include(api_patterns)),
)
