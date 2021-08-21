from django.contrib import admin
from announcements.models import Announcement, Category, Comment
# Register your models here.

admin.site.register(Announcement)
admin.site.register(Category)
admin.site.register(Comment)