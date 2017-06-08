from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import TaskSerializer, UserSerializer, TasklistSerializer, TagSerializer
from .models import Task, Tasklist, Tag
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from todolist.token import account_activation_token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from todolist.token import account_activation_token
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import SearchFilter



class TagslistCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    model = Tag
    serializer_class = TagSerializer
    def get_queryset(self):
        queryset = self.model.objects.all()
        tag_id = self.kwargs.get('tag_id', None)
        if tag_id is not None:
            queryset = queryset.filter(pk = tag_id)
        return queryset
    

class TasklistCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Tasklist
    serializer_class = TasklistSerializer
    def get_queryset(self):
        queryset = self.model.objects.all().filter(user = self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    
class TasklistDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    model = Tasklist
    serializer_class = TasklistSerializer
    def get_queryset(self):
        queryset = self.model.objects.all().filter(user = self.request.user)
        return queryset



class TaskFilter(FilterSet):
    class Meta:
        model = Task
        fields = ('name', 'description',)

class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_class = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_class = TaskFilter
    search_fields = ('name', 'description', 'tags__name')
    
    def get_queryset(self):
        list_id = self.kwargs.get('list_id', None)
        return Tasklist.objects.get(pk=list_id, user=self.request.user).tasks.all()

#    def create(self, request, *args, **kwargs):
#        tag_names = request.data.get('tags', [])
#        for tag_name in tag_names:
#            Tag.objects.get_or_create(name=tag_name)
#        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id', None)
#        tag_names = request.data.get('tags', [])
#        for tag_name in tag_names:
#            Tag.objects.get_or_create(name=tag_name)
        try:
            tasklist = Tasklist.objects.get(pk=list_id)
        except Tasklist.DoesNotExist:
            raise NotFound()
        serializer.save(tasklist=tasklist)


class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        list_id = self.kwargs.get('list_id', None)
        return Tasklist.objects.get(pk=list_id, user=self.request.user).tasks.all()

class UserList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer   
    
class SharedTask(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(shared=self.request.user)    

def create_user(request):
    user = User.objects.create(
        username = request.POST['username']
    )
    user.set_password(request.POST['password'])
    user.is_active = False
    user.save()
    current_site = get_current_site(request)
    subject = 'Activate Your TodoList Account'
    message = render_to_string('todolist/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)
    print(message)
    return redirect('/email_sent')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        return redirect('http://127.0.0.1:8080/auth/')
    
def email_sent(request):
    return render(request, 'todolist/email_sent.html')
