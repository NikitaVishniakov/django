from django.contrib import admin

from .models import Task, Tasklist

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ['tasklist', 'name','date_created', 'priority','description']


class TasklistAdmin(admin.ModelAdmin):
    inlines = [TaskInline]
class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_filter = ['tasklist']
    search_fields = ['name']
    list_display = ('name', 'tasklist','description', 'completed')
    fields = ['tasklist', 'name','date_created', 'priority','description']
    
admin.site.register(Tasklist, TasklistAdmin)
admin.site.register(Task, TaskAdmin)

# Register your models here.
