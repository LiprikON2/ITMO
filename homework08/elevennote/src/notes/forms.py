from django import forms

from .models import Note


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = [
            'title',
            'tags',
            'body',
        ]
        
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs.update({
            'id': 'tag-input',
            'placeholder': 'Add tag...',
            'data-role': "tagsinput",
        })
