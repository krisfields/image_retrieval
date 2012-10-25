from django import forms

class UploadFileForm(forms.Form):
	CHOICES_FOR_HANDLING_EXISTING_VENDORS = (
		(1, 'Ignore All'),
		(2, 'Update All'),
		(3, 'Only Update Those Without Profile Pictures'),
	)
	handle_existing_vendors = forms.ChoiceField(
		label=u'How would you like to handle vendors already in the database?',
		widget=forms.Select,
		initial=1,
		choices=CHOICES_FOR_HANDLING_EXISTING_VENDORS
	)
	file = forms.FileField()
