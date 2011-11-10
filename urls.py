from django.conf.urls.defaults import patterns, include, url


task_patterns = patterns('indigo.views',
	url(r'^(?P<task_id>\d+)/$', 'task_detail'),
	url(r'^add/$', 'create_task'),
)

iteration_patterns = patterns('indigo.views',
	url(r'^task/', include(task_patterns)),

	url(r'^(?P<iteration_id>\d+)/$', 'iteration_detail'),
	url(r'^add/$', 'create_iteration'),
)

project_patterns = patterns('indigo.views',
	url(r'^(?P<project_id>\d+)/iteration/', include(iteration_patterns)),

	url(r'^(?P<project_id>\d+)/$', 'project_detail'),
	url(r'^add/$', 'create_project'),
	url(r'^(?P<filter_type>\w*)$', 'project_list'),
)

urlpatterns = patterns('indigo.views',
	url(r'^$', 'index'),

	# Project URLS
	#url(r'^/projects/(?P<filter_type>\w*)$', 'projects_list'),
	#url(r'^/add_project/$', 'create_project'),

	url(r'^project/', include(project_patterns)),

  # Examples:
  # url(r'^login/', 'user_auth', name='login'),
  # url(r'^logout/', 'user_auth', name='logout'),
  # url(r'^create_user/', 'user_auth', name='create_user'),

  # PROJECT URLS
  # url(r'^projects/$', 'projects_list', name='public'),
  # Example url for the following:
  #   http://example.com/indigo/projects/bob/
  # url(r'^projects/(?P<username>\w+)/$', 'projects_list', name='user_projects'),
  # Example url for the following:
  #   http://example.com/indigo/projects/23/
  # url(r'^projects/(?P<project_id>\d+)/$', 'projects_detail'),

  # ITERATION URLS
  # Example url for the following:
  #   http://example.com/indigo/projects/23/iterations/
  # url(r'^projects/(?P<project_id>\d+)/iterations/$', 'iterations_list'),
  # url(r'^projects/(?P<project_id>\d+)/iterations/(?P<iteration_id>\d+)/$', 'iterations_detail'),

  # TASK URLS
  # Example url for the following:
  #   http://example.com/indigo/projects/23/iterations/tasks/
  # url(r'^projects/(?P<project_id>\d+)/iterations/tasks/$', 'tasks_list'),
  # url(r'^projects/(?P<project_id>\d+)/iterations/tasks/(?P<task_id>\d+)/$', 'tasks_detail'),
)

urlpatterns += patterns('',
	url(r'^registration/$', 'registration'),
	url(r'^login/$', 'django.contrib.auth.views.login'),
)
