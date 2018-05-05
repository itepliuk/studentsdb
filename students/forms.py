from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.core.urlresolvers import reverse

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
