from django import forms

from .models import Post

MAX_TWEET_LENGTH = 240

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError('This post is too long')
        return content