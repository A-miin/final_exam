from django.shortcuts import render
from django.utils import timezone
from rest_framework import status

from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from announcements.models import Announcement


class PublishRejectView(GenericAPIView):
    permission_classes = []
    authentication_classes = []
    def get_object(self):
        return get_object_or_404(Announcement, id=self.kwargs.get('id', 0))

    def post(self, *args, **kwargs):
        obj = self.get_object()
        obj.publicated_at = timezone.now()
        obj.status = 'Publicated'
        obj.save()
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        obj = self.get_object()
        obj.status = 'Rejected'
        obj.save()
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)