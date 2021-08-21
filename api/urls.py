from django.urls import path

from api.views import PublishRejectView

app_name = 'api'
urlpatterns = [
    path('announcement/<int:id>/', PublishRejectView.as_view(), name='publish_reject_view')
]