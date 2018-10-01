from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from ..models import Group
from ..forms import GroupAddForm

# Views for Groups

def groups_list(request):
    groups = Group.objects.all()
    
    # try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id','title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    # paginate groups
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        groups = paginator.page(1)
    except EmptyPage:
        #If page is out of range (e.g. 9999), deliver last page of results
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups_list.html', {'groups': groups})

def groups_detail(request, pk=None):
    instance = get_object_or_404(Group, id=pk)
    return render(request, 'students/groups_detail.html', {'instance': instance})

def groups_add(request):
    form = GroupAddForm(request.POST or None, form_add=True)
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:          
            if form.is_valid():
                title = form.cleaned_data['title']
                form.save()
                messages.success(request, 'Групу {} успішно додано!'.format(title))
                return redirect('groups')
            else:
                return render(request, 'students/groups_add.html', {'form': form})
        elif request.POST.get('cancel_button') is not None:
            messages.success(request, 'Додавання групи відмінено!')
            return redirect('groups')
    else:
        #initial form render        
        return render(request, 'students/groups_add.html', {'form': form})

def groups_edit(request, pk=None):    
    instance = get_object_or_404(Group, id=pk)
    form = GroupAddForm(request.POST or None, instance = instance, form_add=False)
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:          
            if form.is_valid():
                title = form.cleaned_data['title']
                form.save()
                messages.success(request, 'Групу {} успішно оновлено!'.format(title))
                return redirect('groups')
            else:
                return render(request, 'students/groups_add.html', {'form': form})
        elif request.POST.get('cancel_button') is not None:
            messages.success(request, 'Редагування групи відмінено!')
            return redirect('groups')
    else:
        #initial form render        
        return render(request, 'students/groups_add.html', {'form': form, 'instance': instance})


def groups_delete(request, pk=None):
    instance = get_object_or_404(Group, id=pk)
    if request.method == 'POST':
        if request.POST.get('delete_button') is not None:
            instance.delete()
            messages.success(request, 'Групу успішно видалено!')
            return redirect('groups')

        elif request.POST.get('cancel_button'):
            messages.success(request, 'Видалення групи відмінено!') 
            # import pdb; pdb.set_trace()
            return redirect('groups')
    else:
        #initial form render        
        return render(request, 'students/groups_delete.html', {'object': instance})