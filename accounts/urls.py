from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    ProfileUpdateView, 
    ProfileDeleteView, 
    LogoutView,
    UsersListView,
    UserRoleUpdateView,
    RestoreProfileView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
    path('profile/restore/', RestoreProfileView.as_view(), name='profile-restore'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_list/', UsersListView.as_view(), name="user-list"),
    path('user/<int:user_id>/role/', UserRoleUpdateView.as_view(), name='user-role-update'),
]