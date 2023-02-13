from django import forms

from .models import Post, Comment

MAX_TWEET_LENGTH = 280
MAX_COMMENT_LENGTH = 280

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError('This post is too long')
        return content

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_COMMENT_LENGTH:
            raise forms.ValidationError('This comment is too long')
        return content