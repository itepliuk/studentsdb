from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Exam, Group
from ..util import get_current_group

def exams_list(request):
	current_group = get_current_group(request)
	if current_group:
		exams = Exam.objects.filter(exam_group=current_group)
	else:
		exams = Exam.objects.all()
	
	# try to order exams list
	order_by = request.GET.get('order_by', '')
	if order_by in ('id','title', 'exam_date'):
		exams = exams.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			exams = exams.reverse()
	
	# paginate exams
	paginator = Paginator(exams, 2)
	page = request.GET.get('page')
	try:
		exams = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page
		exams = paginator.page(1)
	except EmptyPage:
		#If page is out of range (e.g. 9999), deliver last page of results
		exams = paginator.page(paginator.num_pages)

	return render(request, 'students/exams_list.html', {'exams': exams})

def exams_add(request):
	return HttpResponse('<h1>Exams Add Form</h1>')

def exams_edit(request, gid):
	return HttpResponse('<h1>Edit Exam </h1>')

def exams_delete(request, gid):
	return HttpResponse('<h1>Delete Exam </h1>')