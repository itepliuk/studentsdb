from django.contrib import admin
from .models import Student, Group, Exam, Rating

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Exam)
admin.site.register(Rating)
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
# 	pass