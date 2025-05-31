from django.urls import path
from .api import LoginAPI, RegisterAPI, ListUsersAPI, UserUpdateAPI, LogoutAPI

urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='api-login'),
    path('api/register/', RegisterAPI.as_view(), name='api-register'),
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),
    path('api/list-users/', ListUsersAPI.as_view(), name='api-list-users'),
    path('api/user/<int:user_id>/update/', UserUpdateAPI.as_view(), name='api-user-update'),
]