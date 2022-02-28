from dataclasses import field
from django import forms
from django.forms import ModelForm
from django import forms

from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Add desctiption..',
                    'rows': 5,
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Add title..',
                    'autofocus': True,
                }
            ),
            'demo_link': forms.TextInput(
                attrs={
                    'placeholder': 'Add demo link..',
                }
            ),
            'source_link': forms.TextInput(
                attrs={
                    'placeholder': 'Add source link..'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote',
        }


    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})