from django.conf.urls import url,include
from . import views

app_name = 'tasks'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^(?P<team_id>[0-9]+)/$',views.team_details,name='team_details'),
    url(r'^(?P<team_id>[0-9]+)/team_members/$', views.team_members, name='team_members'),
    url(r'^(?P<team_id>[0-9]+)/(?P<task_id>[0-9]+)/$',views.task_details,name='task_details'),
    url(r'^team/add/$', views.TeamCreate.as_view(), name='addteam'),
    url(r'^(?P<team_id>[0-9]+)/addtask/$', views.TaskCreate.as_view(), name='addtask'),
    url(r'^(?P<team_id>[0-9]+)/(?P<pk>[0-9]+)/updatetask/$', views.TaskUpdate.as_view(), name='updatetask'),
    url(r'^(?P<team_id>[0-9]+)/(?P<task_id>\d+)/deletetask/$', views.taskDelete, name='deletetask'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'accounts/',include( 'django.contrib.auth.urls' )),
    url(r'^alltasks/$',views.allTasks,name='alltasks'),
    url(r'^userCreatedTasks/$',views.tasksCreatedByUser,name='userCreatedTasks'),
    url(r'^(?P<team_id>[0-9]+)/(?P<task_id>[0-9]+)/addcomment/$',views.Comment.as_view(),name='addcomment'),
]