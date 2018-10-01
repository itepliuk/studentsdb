from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from ..models import Rating
from ..forms import RatingAddForm

def ratings_list(request):
    ratings = Rating.objects.all()
    # try to order exams list
    
    order_by = request.GET.get('order_by', '')
    if order_by in ('id','student', 'exam_rating', 'mark'):
        ratings = ratings.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            ratings = ratings.reverse()
    elif order_by in ('teacher'):
        ratings = ratings.order_by('exam_rating__teacher')
        if request.GET.get('reverse', '') == '1':
            ratings = ratings.reverse()
            
    return render(request, 'students/ratings_list.html', {'ratings': ratings})

def ratings_add(request):
    form = RatingAddForm(request.POST or None, form_add=True)
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:          
            if form.is_valid():
                mark = form.cleaned_data['mark']
                student = form.cleaned_data['student']
                form.save()
                messages.success(request, 'Оцінку {} студенту {} успішно додано!'.format(mark, student))
                return redirect('ratings')
            else:
                return render(request, 'students/groups_add.html', {'form': form})
        elif request.POST.get('cancel_button') is not None:
            messages.success(request, 'Додавання оцінки відмінено!')
            return redirect('ratings')
    else:

        return render(request, 'students/ratings_add.html', {'form' : form})

def ratings_edit(request, pk=None):    
    instance = get_object_or_404(Rating, id=pk)
    form = RatingAddForm(request.POST or None, instance = instance, form_add=False)
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:          
            if form.is_valid():
                mark = form.cleaned_data['mark']
                student = form.cleaned_data['student']
                form.save()
                messages.success(request, 'Оцінку студенту {} успішно оновлено на {}!'.format(student, mark))
                return redirect('ratings')
            else:
                return render(request, 'students/ratings_add.html', {'form': form})
        elif request.POST.get('cancel_button') is not None:
            messages.success(request, 'Редагування оцінки відмінено!')
            return redirect('ratings')
    else:
        #initial form render        
        return render(request, 'students/ratings_add.html', {'form': form, 'instance': instance})