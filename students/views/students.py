import imghdr
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views.generic import UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from ..models import Student, Group
from ..forms import StudentUpdateForm
from ..util import paginate, get_current_group

# Views for Students

def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()

    # try to order student list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # simple search
    search = request.GET.get('search')
    if search is not None:
        students = Student.objects.search(query=search)
        # view based seach:
        # students = students.filter(
        #     Q(last_name__icontains=search) |
        #     Q(first_name__icontains=search) |
        #     Q(middle_name__icontains=search) |
        #     Q(notes__icontains=search) |
        #     Q(ticket__iexact=search)).distinct()

    # paginate students
    paginator = Paginator(students, 5)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        students = paginator.page(paginator.num_pages)

    # multiply deleting of students
    if request.method == 'POST' and request.POST.get('delete_all'):
        studdel = Student.objects.filter(id__in=request.POST.getlist('del'))
        if studdel.count() > 0:
            studdel.delete()
            messages.success(request, 'Обраних студентів було успішно видалено!')
        return redirect('home')

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:

            # errors collection
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get(
                'middle_name'), 'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = "Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = "Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = "Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = 'Введіть коректний формат дати (напр. 1991-12-25)'
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = "Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = "Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = 'Оберіть коректну групу'
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')

            if photo:
                if imghdr.what(photo) not in ('jpg', 'jpeg', 'png'):
                    errors['photo'] = 'Фото повинно мати розширення: jpg, jpeg, png'
                elif len(photo) > 5 * 1024 * 1024:
                    errors['photo'] = 'Розмір фото не повинен перевищувати 5 Мб'
                else:
                    data['photo'] = photo

            # save student
            if not errors:
                # create student object from data {}
                student = Student(**data)
                # save it to database
                student.save()

                # alert message django
                messages.success(request, 'Студента {} {} успішно додано!'.format(
                    last_name, first_name))

                # redirect user to students list
                return HttpResponseRedirect(reverse('home'))

            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),
                    'errors': errors })
        elif request.POST.get('cancel_button') is not None:
            # redirect to homepage on cancel button
            return HttpResponseRedirect(
                '{}?status_message=Додавання студента скасовано!'.format(reverse('home')))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title')})


class StudentUpdateView(SuccessMessageMixin, UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm
    success_url = reverse_lazy('home')
    success_message = 'Студента успішно збережено!'

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            self.success_message = 'Редагування студента відмінено!'
            # import pdb; pdb.set_trace()
            return redirect('home')
        else:
            return super().post(request, *args, **kwargs)


class StudentDeleteView(SuccessMessageMixin, DeleteView):
    model = Student
    template_name = 'students/students_delete.html'
    success_url = reverse_lazy('home')
    success_message = 'Студента успішно видалено!'

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.success(request, 'Видалення студента відмінено!')
            # import pdb; pdb.set_trace()
            return redirect('home')
        else:
            return super().post(request, *args, **kwargs)


class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/students_detail.html'
    context_object_name = 'instance'
