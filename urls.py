from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^/', 'indigo.views.main'),
    # url(r'^login/', 'indigo.views.user_auth', name='login'),
    # url(r'^logout/', 'indigo.views.user_auth', name='logout'),
    # url(r'^create_user/', 'indigo.views.user_auth', name='create_user'),

    # PROJECT URLS
    # url(r'^projects/$', 'indigo.views.projects_list', name='public'),
    # Example url for the following:
    #   http://example.com/indigo/projects/bob/
    # url(r'^projects/(?P<username>\w+)/$', 'indigo.views.projects_list', name='user_projects'),
    # Example url for the following:
    #   http://example.com/indigo/projects/23/
    # url(r'^projects/(?P<project_id>\d+)/$', 'indigo.views.projects_detail'),

    # ITERATION URLS
    # Example url for the following:
    #   http://example.com/indigo/projects/23/iterations/
    # url(r'^projects/(?P<project_id>\d+)/iterations/$', 'indigo.views.iterations_list'),
    # url(r'^projects/(?P<project_id>\d+)/iterations/(?P<iteration_id>\d+)/$', 'indigo.views.iterations_detail', name='by_id'),
    # url(r'^projects/(?P<project_id>\d+)/iterations/(?P<iteration_name>\w+)/$', 'indigo.views.iterations_detail', name='by_name'),

    # TASK URLS
    # Example url for the following:
    #   http://example.com/indigo/projects/23/iterations/tasks/
    # url(r'^projects/(?P<project_id>\d+)/iterations/tasks/$', 'indigo.views.tasks_list')
)
