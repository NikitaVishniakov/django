from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import models
#from django.conf.settings import REST_URL
from django.conf import settings
import requests
import json

REST = settings.REST_URL

def todolist(request):
    if request.session.get('token', None):
        response = requests.get(REST + 'todolists/', headers={'Authorization': 'Token ' + request.session['token']})
        todolist = json.loads(response.content)
        return render(request, 'app/todolist.html', {'todolist': todolist})
    else:
        return HttpResponseRedirect('/auth/')

def reg(request):
    response = requests.post(REST + 'users/register/', data=new_user)
    content = response.content
    return HttpResponse(content)

def auth_user(request):    
    if request.method == 'POST':
        form = models.AuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = {'username': username, 'password': password} 
            response = requests.post(REST + 'api-token-auth/', data=user)
            request.session['token'] = json.loads(response.content)['token']
            return HttpResponseRedirect('/todolist/')
    else:
        form = models.AuthForm()
        return render(request, 'app/auth.html', {'form': form})

def reg_user(request):    
    if request.method == 'POST':
        form = models.RegForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = {'username': username, 'password': password,'email': email} 
            response = requests.post(REST + 'users/register/', data=user)
            return HttpResponseRedirect('/activate_account/')
    else:
        form = models.RegForm()
        return render(request, 'app/reg.html', {'form': form})

def activation_sent(request):
    return render(request, 'app/activation_sent.html')

def delete_task(request, list_id, pk, *args, **kwargs):
    delete = requests.delete(REST + 'todolists/{}/tasks/{}/'.format(list_id, pk), headers={'Authorization': 'Token ' + request.session['token']})
    return HttpResponseRedirect('/todolist/')

def task_edit(request,list_id, pk, *args, **kwargs):
    if request.session.get('token', None):
        if request.method == 'POST':
            form = models.TaskCreateForm(request.POST)
            if form.is_valid():
                post_data = {}
                for key in form.cleaned_data:
                    post_data[key] = form.cleaned_data[key]
                post_data['tags'] = []
#                [str.strip(x) for x in post_data['tags'][1:-1].split(',')] if post_data['tags'] else []

                response = requests.put(REST + 'todolists/{}/tasks/{}/'.format(list_id, pk), headers={'Authorization': 'Token ' + request.session['token']}, data=post_data)
                return HttpResponseRedirect('/todolist/')
        else:
            response = requests.get(REST + 'todolists/{}/tasks/{}/'.format(list_id, pk), headers={'Authorization': 'Token ' + request.session['token']})
            form = models.TaskCreateForm(json.loads(response.content))
            return render(request, 'app/update_task.html', {'form': form, 'list_id': list_id, 'pk': pk})

    else:
        return HttpResponseRedirect('/auth/')

def new_task(request, list_id):
    if request.session.get('token', None):
        if request.method == 'POST':
            form = models.TaskCreateForm(request.POST)
            if form.is_valid():
                post_data = {}
                for key in form.cleaned_data:
                    post_data[key] = form.cleaned_data[key]
                post_data['tags'] = []
    #                [str.strip(x) for x in post_data['tags'][1:-1].split(',')] if post_data['tags'] else []

                response = requests.post(REST + 'todolists/{}/tasks/'.format(list_id), headers={'Authorization': 'Token ' + request.session['token']}, data=post_data)
                return HttpResponseRedirect('/todolist/')
        else:
            form = models.TaskCreateForm()
            return render(request, 'app/create_task.html', {'form': form, 'list_id': list_id})

    else:
        return HttpResponseRedirect('/auth/')
    
def new_taskgroup(request):
    if request.session.get('token', None):
        if request.method == 'POST':
            form = models.TaskGroupForm(request.POST)
            if form.is_valid():
                post_data = {}
                for key in form.cleaned_data:
                    post_data[key] = form.cleaned_data[key]
                response = requests.post(REST + 'todolists/', headers={'Authorization': 'Token ' + request.session['token']}, data=post_data)
                return HttpResponseRedirect('/todolist/')
        else:
            form = models.TaskGroupForm()
            return render(request, 'app/create_taskgroup.html', {'form': form,})

    else:
        return HttpResponseRedirect('/auth/')
    
def logout_user(request):
    request.session['token'] = None
    return HttpResponseRedirect('/auth/')


def task_detail(request, list_id, pk):
    if request.session.get('token', None):
        response = requests.get(REST + 'todolists/' + list_id + '/tasks/' + pk, headers={'Authorization': 'Token ' + request.session['token']})
        task = json.loads(response.content)
        return render(request, 'app/task.html', {'task': task})
    else:
        return HttpResponseRedirect('/auth/')
    
#def task_edit(request, list_id, pk):
#    if request.session.get('token', None):
#        response = requests.get(REST + 'todolists/' + list_id + '/tasks/' + pk, headers={'Authorization': 'Token ' + request.session['token']})
#        task = json.loads(response.content)
#        if request.method == 'POST':
#            form = models.TaskEditForm(request.POST)
#            if form.is_valid():
#                name = form.cleaned_data['username']
#                description = form.cleaned_data['description']
#                completed = form.cleaned_data['completed']
#                priority = form.cleaned_data['priority']
#                tags = form.cleaned_data['tags']
#                task = {'name': username, 'completed': completed, 'priority': priority, 'description': description, 'tags': tags} 
#                response = requests.update(REST + '/todolist/' + list_id + '/tasks/' + pk, data= task, headers={'Authorization': 'Token ' + request.session['token']})
#                return HttpResponseRedirect('/todolist/' + list_id + '/tasks/' + pk)
#        else:
#            form = models.TaskEditForm()
#            return render(request, 'app/auth.html', {'form': form})
#
#    else:
#        return HttpResponseRedirect('/auth/')

