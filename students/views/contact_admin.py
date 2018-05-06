from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin

from studentsdb.settings import ADMIN_EMAIL
from ..forms import ContactForm

# Function based view for contact admin

# def contact_admin(request):
# 	#check if form was posted
# 	if request.method == 'POST':
# 		# create a form instance and populate it with data from the request
# 		form = ContactForm(request.POST)

# 		# check weather user data is valid:
# 		if form.is_valid():
# 			# send email
# 			subject = form.cleaned_data['subject']
# 			message = form.cleaned_data['message']
# 			from_email = form.cleaned_data['from_email']

# 			try:
# 				send_mail(subject, message, from_email, [ADMIN_EMAIL])
# 			except Exception as e:
# 				messages.error(request, 'При відправці листа виникла помилка {}'.format(e))
# 			else:
# 				messages.success(request, 'Повідомлення успішно надіслане!')
# 			return redirect('contact_admin')
# 	else:
# 		form = ContactForm()

# 	return render(request, 'contact_admin/form.html', {'form': form})

# Class based view for contact admin
class ContactView(SuccessMessageMixin, FormView):
	template_name = 'contact_admin/form.html'
	form_class = ContactForm
	success_url = '/contact-admin/'

	def form_valid(self, form):
		subject = form.cleaned_data['subject']
		message = form.cleaned_data['message']
		from_email = form.cleaned_data['from_email']

		try:
			send_mail(subject, message, from_email, [ADMIN_EMAIL])
		except Exception as e:
			messages.error(self.request, 'При відправці листа виникла помилка {}'.format(e))
		else:
			self.success_message = 'Повідомлення успішно надіслане!'
		return super().form_valid(form)