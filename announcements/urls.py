from django.urls import path

from announcements.views import IndexView

app_name = 'annoncement'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

]
