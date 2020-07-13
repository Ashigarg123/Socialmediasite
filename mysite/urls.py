"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from Socialize import views
from django.conf.urls.static import static
from django.conf import settings
from Socialize.views import HomeView, AboutView, ContactView
from django.views.generic.base import RedirectView
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    #url('accounts/', include('django_registration.backends.activation.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls'),),
    #url('Socialize/', include('Socialize.urls')),
    path('home/', views.HomeView.as_view(), name="home"),
    #url('', RedirectView.as_view(url="home/")),
    path('about/', views.AboutView.as_view(), name="about"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    url('profile/edit/<int:pk>', views.MyProfileUpdateView.as_view(success_url="/home/"),name="profile" ),
    path('mypost/create/', views.MyPostCreate.as_view(success_url="/mypost/"), name='create'),
    path('mypost/', views.MyPostListView.as_view(), name="post"),
    path('mypost/<int:pk>', views.MyPostDetailView.as_view(template_name = "Socialize/mypost_detail.html"), name="particular"),
    path('mypost/<int:pk>/delete', views.MyPostDeleteView.as_view(success_url="/home/"), name="delete"),
    path('myprofile/<int:pk>', views.MyProfileDetailView.as_view(), name="p1"),
    path('myprofile/', views.MyProfileListView.as_view(), name="myprofile"),
    path('myprofile/follow/<int:pk>', views.follow, name="follow"),
    path('myprofile/unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('mypost/like/<int:pk>', views.like, name="like"),
    path('mypost/unlike/<int:pk>', views.unlike, name="unlike"),
    path('mypost/<int:pk>/change', views.MyPostUpdateView.as_view(success_url="/home/"),name="update" ),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
