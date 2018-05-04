from django import forms

class ContactForm(forms.Form):
	from_email = forms.EmailField(
		label='Ваша Емейл Адреса')

	subject = forms.CharField(
		label='Заголовок листа',
		max_length=128)

	message = forms.CharField(
		label='Текст повідомлення',
		max_length=2560,
		widget=forms.Textarea)