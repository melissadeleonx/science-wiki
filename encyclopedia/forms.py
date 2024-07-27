from django import forms
from markdown2 import markdown

class NewPageForm(forms.Form):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'})
    )
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter content here', 'rows': 10})
    )

class EditEntryForm(NewPageForm):
    def __init__(self, *args, **kwargs):
        initial_content = kwargs.pop('initial_content', '')
        rendered_initial_content = markdown(initial_content)
        super(EditEntryForm, self).__init__(*args, **kwargs)
        self.fields['content'].initial = rendered_initial_content
