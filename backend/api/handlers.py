from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from api.models import FollowStatus


@receiver(post_save, sender=FollowStatus, dispatch_uid='increment_follower_count')
def increment_follower_count(sender, instance, **kwargs):
    instance.content_type.model_class().objects.\
        filter(id=instance.object_id).update(follower_count=F('follower_count')+1)

@receiver(pre_delete, sender=FollowStatus, dispatch_uid='decrement_follower_count')
def decrement_follower_count(sender, instance, **kwargs):
    instance.content_type.model_class().objects.\
        filter(id=instance.object_id).update(follower_count=F('follower_count')-1)
