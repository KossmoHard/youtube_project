from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.shortcuts import reverse

from youtube_project import settings


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Video(models.Model):
    video_id = models.CharField(max_length=150, unique=True)
    title = models.CharField(max_length=150, db_index=True)
    description = models.TextField(blank=True, db_index=True)
    preview = models.ImageField(upload_to='media/', default='media/photo_2019-05-04 17.39.22.jpeg', blank=True)
    published = models.DateTimeField(auto_now_add=False)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_video_url', kwargs={'pk': self.pk})

    @property
    def total_likes(self):
        return self.likes.count()












