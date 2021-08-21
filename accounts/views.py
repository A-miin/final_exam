from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q

# Create your views here.
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from accounts.models import User
from accounts.form import UserUpdateForm

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

class UserUpdateView(UpdateView):
    model = User
    template_name = 'profile_update.html'
    context_object_name = 'user_obj'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.id})



    def get_object(self, queryset=None):
        return self.request.user


