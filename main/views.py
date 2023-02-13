from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    CreateView
)

from .forms import CommentForm
from users.forms import ProfileUpdateForm
from .models import Post, Comment


class PostListView(ListView):
    model = Post
    template_name = 'main/index.html'  # <app>/<model>_viewtype.html
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    # paginate_by = 8
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user_id'] = self.request.user
        return context


class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.kwargs['pk']
        context['comments'] = Comment.objects.filter(post=post)
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'main\components\post_create.html'
    fields = ['content']
    success_message = 'Post  was created successfully'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect('index')

    def form_invalid(self, form):
        return redirect('index')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post

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
        'likes_count': post.total_likes(),
        'like_list_users': post.liking_users_list()
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
                   'likes_count': post.total_likes(),
                   'like_list_users': post.liking_users_list()}
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