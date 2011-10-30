from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('indigo.views',
    # Examples:
    # url(r'^/', 'main'),
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
