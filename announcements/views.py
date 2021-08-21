from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.views import View
from django.utils.http import urlencode
import uuid
from announcements.form import SearchForm, AnnouncementForm
from announcements.models import Announcement

# Create your views here.
class IndexView(ListView):

    template_name = 'index.html'
    model = Announcement
    context_object_name = 'announcements'
    ordering = ('-created_at')
    paginate_by = 9
    paginate_orphans = 0


    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status='Publicated')

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
        context['search_form'] = self.form

        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})

        return context

class AnnouncementView(DetailView):
    model = Announcement
    template_name = 'announcement_detail.html'
    context_object_name = 'announcement'


class CreateAnnouncementView(LoginRequiredMixin, CreateView):
    template_name = 'new_announcements.html'
    form_class = AnnouncementForm
    model = Announcement

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.author = self.request.user
        announcement.save()

        return redirect('annoncement:index')

class ReviewAnnouncementView(ListView):

    template_name = 'review.html'
    model = Announcement
    context_object_name = 'announcements'
    ordering = ('-created_at')
    paginate_by = 9
    paginate_orphans = 0


    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(ReviewAnnouncementView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status='For moderation')

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
        context['search_form'] = self.form

        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})

        return context