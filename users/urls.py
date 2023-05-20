from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views
from .views import RegisterView
from .views import create_post


from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create_post/', create_post, name='create_post'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('search_results/', views.search_results, name='search_results'),
    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('cancel_friend_request/<int:request_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),

]
