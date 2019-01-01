from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from notifications.signals import notify

from api.models import Event, FollowStatus, Message, User


@receiver(post_save, sender=FollowStatus, dispatch_uid='increment_follower_count')
def increment_follower_count(sender, instance, **kwargs):
    instance.content_type.model_class().objects.\
        filter(id=instance.object_id).update(follower_count=F('follower_count')+1)
    if isinstance(instance.content_object, Event):
        ntf = instance.owner.username + ' followed your event!'
        receiver = instance.content_object.owner
    else:
        ntf = instance.owner.username + ' followed you!'
        receiver = instance.content_object
    notify.send(instance.owner, recipient=receiver, verb=ntf)

@receiver(pre_delete, sender=FollowStatus, dispatch_uid='decrement_follower_count')
def decrement_follower_count(sender, instance, **kwargs):
    instance.content_type.model_class().objects.\
        filter(id=instance.object_id).update(follower_count=F('follower_count')-1)

@receiver(post_save, sender=Message, dispatch_uid='send_message_notification')
def send_message_notification(sender, instance, **kwargs):
    ntf = instance.owner.username + ' sent you a message!'
    notify.send(instance.owner, recipient=instance.receiver, verb=ntf)
