from django.contrib import admin
from .models import Subject, Teacher
from .forms import TeacherForm


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Teacher)
class TeachersAdmin(admin.ModelAdmin):
    form = TeacherForm
    list_display = ('id', 'first_name', 'email_address', 'profile_picture')
