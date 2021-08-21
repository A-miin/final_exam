from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

ANNONCEMENT_STATUS = (
        ('For moderation', 'На модерацию'),
        ('Publicated', 'Опубликовано'),
        ('Rejected', 'Отлонено'),
    )

class Category(models.Model):
    name = models.CharField(max_length=128,
                            null=False,
                            blank=False,
                            verbose_name=_('Название'))

    class Meta:
        db_table = 'categories'
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return f'{self.id}. {self.name}'

class Announcement(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name=_('Заголовок'))

    text = models.TextField(max_length=1024,
                            verbose_name=_('Текст объявления'))

    picture = models.ImageField(upload_to='pictures/',
                                verbose_name=_('Картинка'))

    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name='announcements',
                                 verbose_name=_('Категория'))

    price = models.PositiveIntegerField(null=True,
                                        blank=True,
                                        verbose_name=_('Цена'))

    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='announcements')

    publicated_at = models.DateTimeField(null=True,
                                         blank=True,
                                         verbose_name=_('Дата публикации'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=128, choices=ANNONCEMENT_STATUS, default='For moderation')
    is_active = models.BooleanField(default=True)


    class Meta:
        db_table = 'announcements'
        verbose_name = _('Объявление')
        verbose_name_plural = _('Объявления')

    def __str__(self):
        return f'{self.id}. {self.author}: {self.title}'


class Comment(models.Model):
    announcement = models.ForeignKey(
        'announcements.Announcement',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Объявление'),
        null=False,
        blank=False)

    comment = models.CharField(max_length=256,
                               verbose_name=_('Комментарий'),
                               null=False,
                               blank=False)

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
        null=False,
        blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')

    def __str__(self):
        return f'{self.author}: {self.comment}'
