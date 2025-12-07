from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    ProfileUpdateView, 
    ProfileDeleteView, 
    LogoutView,
    UsersListView
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_list/', UsersListView.as_view(), name="user-list")
]