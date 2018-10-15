from django.contrib import admin, messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django.forms.models import BaseModelFormSet
from .models import Student, Group, Exam, Rating, Issue, Answer


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and \
                self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError('Студент є старостою іншої групи', code='invalid')
        return self.cleaned_data['student_group']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo is not None:
            if len(photo) > 5 * 1024 * 1024:
                raise ValidationError('Розмір зображення не може перевищувати 5 Мб')
        return self.cleaned_data['photo']


class StudentBaseFormSet(BaseModelFormSet):
    # TO DO FIX IF NONE SELECTED STUDENTS IN FORMSET

    def clean(self):
        if any(self.errors):
            return
        # print(self.cleaned_data)
        for form in self.forms:
            student_group = form.cleaned_data.get('student_group')
            groups = Group.objects.filter(leader=form.instance)
            if len(groups) > 0 and student_group is not None and \
                    student_group != groups[0]:
                form.add_error('student_group', 'Студент є старостою іншої групи')
                raise ValidationError('Студент є старостою іншої групи', code='invalid')
        return self.cleaned_data


class StudentAdmin(admin.ModelAdmin):
    list_display = ['photo_display', 'last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    actions = ['copy_students']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}

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

    def photo_display(self, obj):
        img_tag = '<img class="rounded-circle" height="30" width="30" src="{}">'
        if obj.photo:
            return img_tag.format(obj.photo.url)
        else:
            if obj.gender == obj.male:
                return img_tag.format(settings.STATIC_URL + 'img/male.png')
            else:
                return img_tag.format(settings.STATIC_URL + 'img/female.png')

    photo_display.short_description = 'Фото'
    photo_display.allow_tags = True


class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        if self.cleaned_data['leader'] is not None:
            if self.cleaned_data['leader'].student_group != self.instance:
                raise ValidationError('Вибраний староста не є студентом цієї групи', code='invalid')


class GroupBaseFormSet(BaseModelFormSet):
    # TO DO FIX IF NONE SELECTED GROUPS IN FORMSET
    def clean(self):
        if any(self.errors):
            return
        # print(self.cleaned_data)
        for form in self.forms:
            if form.cleaned_data['leader'] is not None:
                if form.cleaned_data['leader'].student_group != form.instance:
                    form.add_error('leader', 'Цей староста не є студентом цієї групи')
                    raise ValidationError(
                        'Вибраний староста не є студентом цієї групи', code='invalid')
        return self.cleaned_data


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader', 'notes']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_filter = ['leader']
    list_per_page = 10
    search_fields = ['title', 'leader', 'notes']
    prepopulated_fields = {'slug': ('title',)}

    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})

    def get_changelist_formset(self, request, **kwargs):
        kwargs['formset'] = GroupBaseFormSet
        return super().get_changelist_formset(request, **kwargs)


#Answers functionallity in admin part
class AnswerInline(admin.StackedInline):
    model = Answer


class IssueAdmin(admin.ModelAdmin):
    list_display = ['from_email', 'subject', 'get_user', 'is_replied']
    #readonly_fields = ['from_email', 'subject', 'message', 'get_user', 'is_replied']
    inlines = [AnswerInline]
    def get_user(self, obj):
        return obj.answer.user if obj.answer.user else '-'

    get_user.short_description = 'Відповідь надано'




# Register your models here.
admin.site.register(Student, StudentAdmin)

admin.site.register(Exam)
admin.site.register(Rating)

admin.site.register(Issue, IssueAdmin)
