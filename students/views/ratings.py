from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Rating

def ratings_list(request):
    ratings = Rating.objects.all()
    # try to order exams list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id','student'):
        ratings = ratings.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            ratings = ratings.reverse()

    return render(request, 'students/ratings_list.html', {'ratings': ratings})