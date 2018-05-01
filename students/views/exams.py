from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Exam, Group

def exams_list(request):
	exams = Exam.objects.all()
	# try to order exams list
	order_by = request.GET.get('order_by', '')
	if order_by in ('id','title', 'exam_date'):
		exams = exams.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			exams = exams.reverse()

	return render(request, 'students/exams_list.html', {'exams': exams})

def exams_add(request):
	return HttpResponse('<h1>Exams Add Form</h1>')

def exams_edit(request, gid):
	return HttpResponse('<h1>Edit Exam </h1>')

def exams_delete(request, gid):
	return HttpResponse('<h1>Delete Exam </h1>')