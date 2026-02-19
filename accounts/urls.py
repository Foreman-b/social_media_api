from django.urls import path, include
from .views import LoginView, RegisterView, UserProfileView, FollowUserView, UnfollowUserView
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Follow and Unfollow endpoints
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),

]   


