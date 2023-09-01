from django.db.models.signals import pre_save,post_save,post_delete
from .models import *
from django.dispatch import receiver

@receiver(post_save, sender=Follow)
def update_follow_counts(sender, instance, created, **kwargs):
    if created:

        followed_user = instance.followed_user
        following_user = instance.following_user

        followed_user_profile = User.objects.get(user=followed_user)
        followed_user_profile.followers_count += 1 
        followed_user_profile.save()

        following_user_profile = User.objects.get(user=following_user)
        following_user_profile.following_count += 1
        following_user_profile.save()

@receiver(post_delete, sender=Follow)
def update_follow_counts_on_delete(sender, instance, **kwargs):
    followed_user = instance.followed_user
    following_user = instance.following_user

    followed_user_profile = User.objects.get(user=followed_user)
    followed_user_profile.followers_count -= 1
    followed_user_profile.save()

    following_user_profile = User.objects.get(user=following_user)
    following_user_profile.following_count -= 1
    following_user_profile.save()