from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Add title...', 
                'autofocus': True
            }
        )
    class Meta:
        model = Post
        fields = ('title', 'description', 'body', 'featured_image', 'is_featured')

class CreatePostForm(PostForm):
    pass
