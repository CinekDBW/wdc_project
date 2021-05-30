from django.contrib import messages
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse


class Topic(models.Model):

    class Meta:
        permissions = (
            ("can_verify_topics", "Can verify topics"),
            ("can_view_all_topics", "Can view all topics"),
                       )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    date_posted = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)
    allowed_users = models.ManyToManyField(User, related_name='allowed_users', blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum-home')

    def get_all_posts(self):
        return Post.objects.filter('topic' == self)


class Post(models.Model):
    class Meta:
        permissions = (("can_delete_every_post", "Can delete every post"),)

    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="posts_from_topic")

    def __str__(self):
        return f'{self.author}_{self.date_posted}'

    def get_absolute_url(self):
        return reverse('topic-details', kwargs={'pk': self.topic_id})
