from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.homePage, name="homePage"),
    path('post/add/', views.addPost, name='addPost'),
    path('post/view/<int:pk>/', views.postDetail, name='postDetail'),
    path('post/delete/<int:pk>/', views.postDelete, name='postDelete'),
    path('account/register/', views.register, name='register'),
    path('post/edit/<int:pk>/', views.editPost, name='editPost'),
    path('account/home', views.UserHomePage, name='redirect'),
    path('account/login', views.user_login, name='login'),
    path('account/logout', views.user_logout, name='logout'),
    path('profile/<username>', views.profile, name='profile')
]