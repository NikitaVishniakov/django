"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views
    
urlpatterns = {
    url(r'^register/$', views.reg_user),
    url(r'^auth/$', views.auth_user),
#    url(r'^auth_form/$', views.auth_form),
    url(r'^todolist/$', views.todolist),
    url(r'^$', views.todolist),
    url(r'^todolist/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', views.task_detail),
    url(r'^todolist/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/edit/$', views.task_edit),
    url(r'^todolist/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/delete/$', views.delete_task),
    url(r'^todolist/(?P<list_id>[0-9]+)/new/$', views.new_task),
    url(r'^todolist/new/$', views.new_taskgroup),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/', views.logout_user),
    url(r'^activate_account/', views.activation_sent),

#    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#        views.activate, name="activate"),
}

#urlpatterns = format_suffix_patterns(urlpatterns)

    
