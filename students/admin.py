from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django.forms.models import BaseModelFormSet
from .models import Student, Group, Exam, Rating


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and \
            self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError('Студент є старостою іншої групи', code='invalid')
        return self.cleaned_data['student_group']


class StudentBaseFormSet(BaseModelFormSet):
    # TO DO FIX IF NONE SELECTED STUDENTS IN FORMSET

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        #print(self.cleaned_data)
        for form in self.forms:
            student_group = form.cleaned_data.get('student_group')
            groups = Group.objects.filter(leader=form.instance)
            if len(groups) > 0 and student_group != None and \
                student_group != groups[0]:
                raise ValidationError('Студент є старостою іншої групи', code='invalid')
        return self.cleaned_data
        

class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page =  10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    actions = ['copy_students']

    form = StudentFormAdmin

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

    def copy_students(self, request, queryset):
        for obj in queryset:
            obj.id = None
            obj.save()
        messages.success(request, 'Обраних студентів було успішно скопійовано') 
    copy_students.short_description = 'Сopy selected students'

    def get_changelist_formset(self, request, **kwargs):
        kwargs['formset'] = StudentBaseFormSet
        return super().get_changelist_formset(request, **kwargs)

class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        if self.cleaned_data['leader'].student_group != self.instance:
            raise ValidationError('Вибраний староста не є студентом цієї групи', code='invalid')
        return self.cleaned_data['leader']

class GroupBaseFormSet(BaseModelFormSet):
    # TO DO FIX IF NONE SELECTED GROUPS IN FORMSET
    def clean(self):
        #print(self.cleaned_data)
        for form in self.forms:
            print(form.cleaned_data)
            try:
                if form.cleaned_data['leader'] != None:
                    if form.cleaned_data['leader'].student_group != form.instance:
                        raise ValidationError('Вибраний староста не є студентом цієї групи', code='invalid')
            except KeyError:
                pass

                
        return self.cleaned_data           
        

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader', 'notes']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_filter = ['leader']
    list_per_page =  10
    search_fields = ['title', 'leader', 'notes']

    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})

    def get_changelist_formset(self, request, **kwargs):
        kwargs['formset'] = GroupBaseFormSet
        return super().get_changelist_formset(request, **kwargs)



# Register your models here.
admin.site.register(Student, StudentAdmin)

admin.site.register(Exam)
admin.site.register(Rating)
