from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from users.views import (
    UserProfileView,
    profile_redirect,
    logout_view,
    signup_view
)
from main.views import (
    IndexView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    like_post,
    settings_view,
    get_posts_json,
    CommentCreateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    # post URLs
    path('post/create', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>', like_post, name='like-post'),
    path('post/<int:pk>/addcomment', CommentCreateView.as_view()),
    # post JSON URLs
    path('json/posts/all', get_posts_json, name='posts-json'),
    # profile URLs
    path('profile/<slug:slug>', UserProfileView.as_view(), name='profile'),
    path('profile-self/', profile_redirect, name='profile-self'),
    path('settings/', settings_view, name='settings'),
    # authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('pwreset/', auth_views.PasswordResetView.as_view(template_name='users/pwreset.html'), name='pwreset'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
