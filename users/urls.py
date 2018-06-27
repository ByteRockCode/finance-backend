from django.urls import path

from .views import signup
from .views import UserUpdateView


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
]
