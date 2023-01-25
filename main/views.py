from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

from users.forms import ProfileUpdateForm
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'main/index.html' # <app>/<model>_viewtype.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'main\components\post_create.html'
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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


def settings_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.Profile)
        if form.is_valid:
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('settings')
    else:
        form = ProfileUpdateForm()
    return render(request, 'main/settings.html', {'profile_edit_form': form})