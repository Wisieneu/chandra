from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from users.views import (
    UserProfileView,
    profile_redirect,
    logout_view,
    signup_view,
    settings_view
)
from main.views import (
    IndexView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    like_post,
    like_comment,
    CommentCreateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # post URLs
    path('', IndexView.as_view(), name='index'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>', PostUpdateView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>', like_post, name='like-post'),
    path('post/<int:pk>/addcomment', CommentCreateView.as_view(), name='comment-create'),
    path('likecomment/<int:comment_id>', like_comment, name='like-comment'),
    
    # post JSON URLs
    # path('json/posts/all', get_posts_json, name='posts-json'),
    # path('json/post/<int:pk>', get_posts_json, name='posts-detail-json'),
    
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
