from django import forms

from .models import Post, Comment

MAX_TWEET_LENGTH = 280
MAX_COMMENT_LENGTH = 280


class PostCreateForm(forms.ModelForm):
    content = forms.CharField(max_length=280, required=True, label='', widget=forms.Textarea(
        attrs={'class': 'post-textarea', 'name': 'content', 'placeholder': "What's happening?"}))
    image = forms.ImageField(required=False, label='', widget=forms.FileInput(
        attrs={'class': 'clearablefileinput form-control-file', "accept":"image/*", "id":"img-input"}))

    class Meta:
        model = Post
        fields = ['content', 'image']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError('This post is too long')
        return content


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=280, required=True, label='', widget=forms.Textarea(
        attrs={'class': 'comment-textarea', 'name': 'content', 'placeholder': 'Comment on the post...'}))
    image = forms.ImageField(required=False, label='')

    class Meta:
        model = Comment
        fields = ['content', 'image']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_COMMENT_LENGTH:
            raise forms.ValidationError('This comment is too long')
        return content
