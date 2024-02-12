"""
URL configuration for instagramam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SigninView.as_view(),name='signin'),
    path('home', views.Home.as_view(),name='home'),
    path('signup', views.SignupView.as_view(),name='signup'),
    path('send_message/', views.send_message, name='send_message'),
    path('addpost', views.AddPostView.as_view(), name='addpost'),
    path('addstory', views.AddStoryView.as_view(), name='addstory'),
    path('explore', views.ExploreView.as_view(), name='explore'),
    path('profile/<int:id>', views.UserProfileView.as_view(), name='profile'),
    path('story/<int:id>',views.StoryView.as_view(),name='story'),
    path('chat/', views.Chat.as_view(), name='chat'),
    path('dm/<int:id>',views.DirectMessageView.as_view(),name='dm'),
    path('send_dm/<int:id>', views.send_dm, name='send_dm'),
    path('comment/<int:id>', views.CommentView.as_view(), name='comment'),
    # path('like/<int:id>', views.like_post, name='like'),
    path('coming soon', views.ComingSoon.as_view(), name='comingsoon'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
