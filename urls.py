from django.conf.urls.defaults import patterns, include, url


task_patterns = patterns('',
	url(r'^(?P<task_number>\d+)/$', 'indigo.views.task_detail'),
	url(r'^add/$', 'indigo.forms_view.create_task'),
	url(r'^(?P<task_number>\d+)/edit/$', 'indigo.forms_view.modify_task'),
	url(r'^(?P<task_number>\d+)/move/$', 'indigo.forms_view.move_task'),
)

iteration_patterns = patterns('',
	url(r'^(?P<iteration_number>\d+)/task/', include(task_patterns)),

	url(r'^(?P<iteration_number>\d+)/$', 'indigo.views.iteration_detail'),
	url(r'^add/$', 'indigo.forms_view.create_iteration'),
)

project_patterns = patterns('',
	url(r'^(?P<project_id>\d+)/iteration/', include(iteration_patterns)),

	url(r'^(?P<project_id>\d+)/$', 'indigo.views.project_detail'),
	url(r'^(?P<project_id>\d+)/edit/$', 'indigo.forms_view.modify_project'),
	url(r'^add/$', 'indigo.forms_view.create_project'),

  url(r'^$', 'indigo.views.project_list'),
	url(r'^(?P<filter_type>\w*)/$', 'indigo.views.project_list'),
	url(r'^(?P<project_id>\d+)/associate/$', 'indigo.forms_view.project_associate'),
)

urlpatterns = patterns('',
	url(r'^$', 'indigo.views.index'),

	url(r'^registration/$', 'indigo.forms_view.registration'),

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
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/indigo/'}),
)
