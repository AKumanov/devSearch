from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {
                'class': 'input',
                'placeholder': 'Add title...',
                'autofocus': True
            }
        ),
        self.fields['description'].widget.attrs.update(
            {
                'class': 'input',
                'placeholder': 'Add description...',
            }
        )
        self.fields['topic'].widget.attrs.update(
            {
                'class': 'input',
            }
        )

    class Meta:
        model = Post
        fields = ('title', 'topic', 'description', 'body', 'featured_image')


class CreatePostForm(PostForm):
    pass


class UpdatePostForm(PostForm):
    pass
