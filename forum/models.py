from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Topic(models.Model):

    class Meta:
        permissions = (("can_view_private_topics", "Can view private Topics"),)

    title = models.CharField(max_length=400)
    date_posted = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

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