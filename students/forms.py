from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django import forms
from django.core.urlresolvers import reverse

from .models import Student, Group, Exam, Rating


class ContactForm(forms.Form):

	from_email = forms.EmailField(
		label='Ваша E-mail Адреса')

	subject = forms.CharField(
		label='Заголовок листа',
		max_length=128,
		required=True)

	message = forms.CharField(
		label='Текст повідомлення',
		max_length=2560,
		widget=forms.Textarea)

	def __init__(self, *args, **kwargs):
		# call original initializator
		super().__init__(*args, **kwargs)

		# this helper object allows us to customize form
		self.helper = FormHelper()

		# form tag attributes
		self.helper.form_class = 'form-horisontal'
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('contact_admin')

		# twitter bootstrap styles
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 col-form-label'
		self.helper.field_class = 'col-sm-4'

		# form buttons
		self.helper.add_input(Submit('send_button', 'Надіслати'))


class StudentUpdateForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horisontal'

		# twitter bootstrap styles
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 col-form-label'
		self.helper.field_class = 'col-sm-4'

		# add buttons
		self.helper.layout.append(FormActions(
			Submit('add_button','Зберегти', css_class='btn btn-primary'),
			Submit('cancel_button', 'Скасувати', css_class='btn btn-link'),
			))

class GroupAddForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		self.helper.form_action = reverse('groups_add')
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horisontal'

		# twitter bootstrap styles
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 col-form-label'
		self.helper.field_class = 'col-sm-4'

		# add buttons
		self.helper.layout.append(FormActions(
			Submit('add_button','Зберегти', css_class='btn btn-primary'),
			Submit('cancel_button', 'Скасувати', css_class='btn btn-link', formnovalidate='formnovalidate'),
			))