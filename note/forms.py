from django import forms
from django.shortcuts import get_object_or_404

from note.models import Note, Category


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'content', )


class CategoryForm(forms.ModelForm):
    add = forms.BooleanField(required=False)

    class Meta:
        model = Category
        fields = ('name', 'color', 'add')

    def save(self, commit=True, **kwargs):
        category_obj = super(CategoryForm, self).save(commit=False)
        if commit:
            category_obj.save()

            add = self.cleaned_data.get('add', None)
            if add:
                note_obj = get_object_or_404(Note, slug=kwargs.get('note_slug'))
                note_obj.categories.add(category_obj)

        return category_obj
