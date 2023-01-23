"""chandra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from turtle import home
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from main import views as home_views
from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.PostListView.as_view(), name='index'),
    path('post/<pk>/', home_views.PostDetailView.as_view(), name='post-detail'),
    path('post/create', home_views.PostCreateView.as_view(), name='post-create'),
    path('post/<pk>/update/', home_views.PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', home_views.PostDeleteView.as_view(), name='post-delete'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('signup/', user_views.signup, name='signup'),
    path('logout/', user_views.logout_view, name='logout'),
    path('profile/', user_views.profile, name='profile-self'),
    path('settings/', home_views.settings_view, name='settings'),
    # path('profile/<int:pk>', user_views.)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)