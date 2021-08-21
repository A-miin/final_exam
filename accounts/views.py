from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from announcements.models import Announcement
from accounts.models import User


class UserView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        if self.request.user==user:
            context['announcements'] = user.announcements.filter(is_active=True)
        else:
            context['announcements'] = user.announcements.filter(Q(status='Publicated') & Q(is_active=True))

        return context


