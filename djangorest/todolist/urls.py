from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .views import TasklistCreateView, TasklistDetailsView, TaskCreateView, TaskDetailsView, SharedTask
from . import views
from rest_framework import routers
from rest_framework import authtoken
from django.views.decorators.csrf import csrf_exempt


#router = routers.DefaultRouter()
#
#router.register(r'tasks', TaskCreateView)
#router.register(r'tags', TagslistCreateView)

urlpatterns = {
    url(r'^users/register/$', csrf_exempt(views.create_user), name='user'),
    url(r'^todolists/$', TasklistCreateView.as_view(), name="lists"),
    url(r'^todolists/tags$', views.TagslistCreateView.as_view(), name="tag-list"),
    url(r'^todolists/tags/(?P<pk>[0-9]+)/$', views.TagDetailView.as_view(), name="tag-list"),
    url(r'^todolists/(?P<pk>[0-9]+)/$', TasklistDetailsView.as_view(), name="list-detail"),
    url(r'^api-token-auth/$', authtoken.views.obtain_auth_token),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/$', TaskCreateView.as_view(), name="create"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', TaskDetailsView.as_view(), name="task-detail"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name="activate"),
    url(r'^shared/$', views.SharedTask.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^email_sent/$', views.email_sent),


}

urlpatterns = format_suffix_patterns(urlpatterns)
