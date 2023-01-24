from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from users.views import (
    UserProfileView,
    OwnProfileView,
    logout_view,
    signup_view
)
from main.views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    settings_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='index'),
    # post URLs
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/create', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # profile URLs
    path('profile/<str:username>', UserProfileView.as_view(), name='profile'),
    path('profile/', OwnProfileView.as_view(), name='profile-self'),
    path('settings/', settings_view, name='settings'),
    # authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)