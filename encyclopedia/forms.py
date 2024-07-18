from django import forms
from markdown2 import markdown


class NewPageForm(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(label='', widget=forms.Textarea)

class EditEntryForm(NewPageForm):
    def __init__(self, *args, **kwargs):
        initial_content = kwargs.pop('initial_content', '')
        rendered_initial_content = markdown(initial_content)
        super(EditEntryForm, self).__init__(*args, **kwargs)
        self.fields['content'].initial = rendered_initial_content
