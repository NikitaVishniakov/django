from django.db import models
from django import forms
import datetime

class AuthForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=100, required = True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(), required = True)
# Create your models here.
class AddTaskGroupForm(forms.Form):
    name = forms.CharField(label='Логин', max_length=100, required = True)

class RegForm(AuthForm):
    email = forms.EmailField(max_length=254,)
    

class TaskCreateForm(forms.Form):
    name = forms.CharField(label = 'Название', max_length=50, required = True)
    description = forms.CharField(widget=forms.Textarea, max_length=1000, label='Описание')
    completed = forms.BooleanField(required=False, label="Завершено")
    date_created = forms.DateField(initial=datetime.date.today, label="Дата создания")
    tags = forms.CharField(label = "Тэги", max_length=100, required=False)
    shared = forms.CharField(label = "Поделиться(Id пользователя)", max_length=100, required=False)

class TaskGroupForm(forms.Form):
    name = forms.CharField(label = 'Название', max_length=50, required = True)
