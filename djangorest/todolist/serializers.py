from rest_framework import serializers
from .models import Task, Tasklist, Tag
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'tasks')
        
class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field="name", queryset = Tag.objects.all())
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'completed', 'date_created', 'tags') #user
        read_only_fields = ('date_created', 'date_modified')
   
    
class TasklistSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only = True)
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Tasklist
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'username', 'lists', 'password')

 
