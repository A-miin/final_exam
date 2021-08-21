from django import forms
from announcements.models import Announcement

class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Найти')


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'text','picture', 'category', 'price')

class AnnouncementApproveForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('status', 'publicated_at')

class AnnouncementUpdateForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title','text','category','picture','price')