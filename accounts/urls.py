from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import UserView, UserUpdateView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/profile/', UserView.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='update'),

]
