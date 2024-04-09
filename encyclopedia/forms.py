from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(label='', widget=forms.Textarea)

class EditEntryForm(NewPageForm):
    def __init__(self, *args, **kwargs):
        initial_content = kwargs.pop('initial_content', '')
        super(EditEntryForm, self).__init__(*args, **kwargs)
        self.fields['content'].initial = initial_content