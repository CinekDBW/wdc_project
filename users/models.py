from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def user_saved(sender, instance, **kwargs):
    if len(instance.groups.all()) <= 0:
        group_casual = Group.objects.get(name='Casual')
        group_casual.user_set.add(User.objects.get(username=instance.username))