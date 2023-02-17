from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic.edit import ModelFormMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    CreateView
)

from .forms import CommentForm, PostCreateForm
from users.forms import ProfileUpdateForm
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
            comment_instance.post = Post.objects.filter(id=self.kwargs['post_id']).first()
            print(self.kwargs['post_id'])
            comment_instance.save()
            return HttpResponseRedirect(comment_instance.get_absolute_url())
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def post(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def post(self, request, *args, **kwargs): 
        self.object = self.get_object() 
        self.object.delete() 
        return redirect(self.get_success_url())
    
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
        return redirect('/')
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

def settings_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.Profile)
        if form.is_valid:
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('settings')
    else:
        form = ProfileUpdateForm()
    return render(request, 'main/settings.html', {'profile_edit_form': form})



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
    data = {
        'id': post_id,
    }
    status = 200
    try:
        obj = Post.objects.get(id=post_id)
        data['id'] = post_id
        data['content'] = obj.content
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