from django.urls import path

from announcements.views import (IndexView,
                                AnnouncementView,
                                CreateAnnouncementView,
ReviewAnnouncementView,
AnnouncementUpdateView,
AnnouncementDeleteView
                                 )

app_name = 'annoncement'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', AnnouncementView.as_view(), name='announcement-detail'),
    path('add/', CreateAnnouncementView.as_view(), name='announcement-create'),
    path('moderator/', ReviewAnnouncementView.as_view(), name='announcement-review'),
    path('<int:pk>/approve', AnnouncementUpdateView.as_view(), name='announcement-review-detail'),
    path('<int:pk>/delete', AnnouncementDeleteView.as_view(), name='announcement-delete'),
]
