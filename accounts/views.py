from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.list import MultipleObjectMixin, ListView

from accounts.models import User
from accounts.form import UserUpdateForm


from django.views.generic import (
    DetailView,
    UpdateView,

)

from django.db.models import Q
from django.utils.http import urlencode
from announcements.form import SearchForm

# Create your views here.
from announcements.models import Announcement

class UserView(ListView):

    template_name = 'profile.html'
    model = Announcement
    context_object_name = 'announcements'
    ordering = ('-created_at')
    paginate_by = 9
    paginate_orphans = 0


    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()

        return super(UserView, self).get(request, **kwargs)

    def get_queryset(self):
        user = self.get_object()
        queryset = super().get_queryset()
        if self.request.user == user:
            queryset = queryset.filter(Q(is_active=True) & Q(author=user))
        else:
            queryset = queryset.filter(Q(author=user) & Q(status='Publicated') & Q(is_active=True))


        if self.search_data:
            queryset = queryset.filter(
                Q(title__icontains=self.search_data) |
                Q(text__icontains=self.search_data)
            )
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_obj']=self.get_object()


        context['search_form'] = self.form


        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})

        return context

    def get_object(self):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        print(user)
        return user

# class UserView(ListView):
#     model = User
#     template_name = 'profile.html'
#     context_object_name = 'announcements'
#     paginate_by = 9
#     paginate_orphans = 0
#
#     def get(self, request, **kwargs):
#         self.form = SearchForm(request.GET)
#         self.search_data = self.get_search_data()
#         return super(UserView, self).get(request, **kwargs)
#
#
#     def get_search_data(self):
#         if self.form.is_valid():
#             return self.form.cleaned_data['search_value']
#         return None
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.get_object()
#         queryset = Announcement.objects.all()
#         if self.search_data:
#             queryset = Announcement.objects.filter(
#                 Q(title__icontains=self.search_data) |
#                 Q(text__icontains=self.search_data)
#             )
#         if self.request.user==user:
#             context['announcements'] = queryset.filter(Q(is_active=True) & Q(author=user))
#         else:
#             context['announcements'] = queryset.filter(Q(author=user) & Q(status='Publicated') & Q(is_active=True))
#
#         context['search_form'] = self.form
#
#         if self.search_data:
#             context['query'] = urlencode({'search_value': self.search_data})
#
#         return context
#




class UserUpdateView(UpdateView):
    model = User
    template_name = 'profile_update.html'
    context_object_name = 'user_obj'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.id})



    def get_object(self, queryset=None):
        return self.request.user


