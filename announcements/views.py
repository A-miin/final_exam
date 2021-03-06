
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.http import urlencode
from announcements.form import SearchForm, AnnouncementForm, AnnouncementUpdateForm
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
        queryset = queryset.filter(Q(status='Publicated') & Q(is_active=True))

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.author == self.request.user:
            context['is_author'] = True

        return context


class CreateAnnouncementView(LoginRequiredMixin, CreateView):
    template_name = 'new_announcements.html'
    form_class = AnnouncementForm
    model = Announcement

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.author = self.request.user
        announcement.save()

        return redirect('annoncement:index')

class ReviewAnnouncementView(PermissionRequiredMixin, ListView):

    def has_permission(self):
        return self.request.user.is_staff


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
        queryset = queryset.filter(Q(status='For moderation') & Q(is_active=True))

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

class AnnouncementApproveView(PermissionRequiredMixin, DetailView):
    model = Announcement
    template_name = 'announcement_approve.html'
    context_object_name = 'announcement'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(status='For moderation') & Q(is_active=True))
        return queryset

    def has_permission(self):
        return self.request.user.is_staff

class AnnouncementDeleteView(PermissionRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'delete.html'
    success_url = reverse_lazy('annoncement:index')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(status='Publicated') & Q(is_active=True))
        return queryset

    def has_permission(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return redirect('annoncement:index')

class AnnouncementUpdateView(PermissionRequiredMixin, UpdateView):
    model = Announcement
    template_name = 'announcement_edit.html'
    context_object_name = 'announcement'
    form_class = AnnouncementUpdateForm

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(status='Publicated') & Q(is_active=True))
        return queryset

    def has_permission(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.status = 'For moderation'
        announcement.save()
        return redirect('annoncement:index')

