from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic.edit import ModelFormMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    CreateView,
)

from .forms import CommentForm, PostCreateForm
from main.models import Post, Comment


class IndexView(ListView, ModelFormMixin):
    model = Post
    template_name = 'main/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 8
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        self.object = None
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, *args, **kwargs):
        self.object = None
        if not self.request.user.is_authenticated:
            raise BaseException()
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            post_instance = self.form.save(commit=False)
            post_instance.author = self.request.user
            post_instance.save()
            return HttpResponseRedirect(post_instance.get_absolute_url())


class PostDetailView(ListView, ModelFormMixin):
    ordering = ['-date_added']
    model = Comment
    context_object_name = 'comments'
    template_name = 'main/post_detail.html'
    paginate_by = 8
    form_class = CommentForm

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(post__id=self.kwargs['post_id'])

    def get_context_data(self):
        self.object = None
        context = super().get_context_data()
        context['post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, *args, **kwargs):
        self.object = None
        if not self.request.user.is_authenticated:
            raise BaseException()
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            comment_instance = self.form.save(commit=False)
            comment_instance.author = self.request.user
            comment_instance.post = Post.objects.filter(
                id=self.kwargs['post_id']).first()
            comment_instance.save()
            return HttpResponseRedirect(comment_instance.get_absolute_url())


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'main/components/post-edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return PermissionDenied


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def get(self, *args, **kwargs):
        raise PermissionDenied

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
    response = {
        'likes_amount': post.likes_amount,
        'liking_users_list': post.liking_users_list
    }
    return JsonResponse(data=response)


@login_required
def like_comment(request, comment_id):
    if request.method != 'POST':
        raise Http404
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
    else:
        comment.likes.remove(request.user)
    response = {
        'likes_amount': comment.likes_amount,
        'liking_users_list': comment.liking_users_list
    }
    return JsonResponse(data=response)


# REST API views for JSON posts data - for potential use for later

def get_posts_json(request, *args, **kwargs):
    posts_qs = Post.objects.all()
    posts_list = [{'id': post.id,
                   'author': {
                       'username': post.author.username,
                       'display_name': post.author.profile.display_name,
                       'pfp_url': post.author.profile.profile_picture.url,
                   },
                   'date_posted': post.date_posted,
                   'content': post.content,
                   'likes_count': post.likes_amount,
                   'like_list_users': post.liking_users_list}
                  for post in posts_qs]
    return JsonResponse(data={'response': posts_list})


def get_post_detail_json(request, post_id, *args, **kwargs):
    # REST API VIEW
    # To be consumed by JS
    # Returns JSON data of a Post object
    status = 200
    try:
        obj = Post.objects.get(id=post_id)
        data = model_to_dict(obj)
    except:
        data = 'Not found'
        status = 404
    return JsonResponse(data=data, status=status)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_message = 'Post was created successfully'

    def form_valid(self, form, **kwargs):
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect('index')

    def form_invalid(self, form):
        return redirect(f'/post/{self.kwargs["pk"]}')