from django.contrib import admin
from .models import ClassGroup, Assignment
from django.contrib import admin
from .models import ClassGroup


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'created_at')
    search_fields = ('name', 'teacher__username')
    filter_horizontal = ('students',)
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'teacher', 'status', 'max_score', 'due_date', 'created_at')
    list_filter = ('status', 'group', 'teacher', 'created_at')
    search_fields = ('title', 'description', 'group__name', 'teacher__username')