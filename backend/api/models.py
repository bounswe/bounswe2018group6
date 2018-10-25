from django.conf import settings
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class OwnerMixin(models.Model):
    """
    Each model that belongs to a `User` must use this mixin.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_set', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CommentMixin(models.Model):
    """
    Each model that contains `Comment`s must use this mixin.
    """
    comments = GenericRelation('Comment')

    class Meta:
        abstract = True


class FollowMixin(models.Model):
    """
    Each model that can be followed by a user must use this mixin.
    """
    followers = GenericRelation('FollowStatus')
    follower_count = models.IntegerField(default=0)

    class Meta:
        abstract = True


class LocationMixin(models.Model):
    """
    Each model that contains a `Location` must use this mixin.
    """
    location = GenericRelation('Location')

    class Meta:
        abstract = True


class MediaMixin(models.Model):
    """
    Each model that contains `Media`s must use this mixin.
    """
    medias = GenericRelation('Media')

    class Meta:
        abstract = True


class VoteMixin(models.Model):
    """
    Each model that can be voted by a user must use this mixin.
    """
    votes = GenericRelation('VoteStatus')
    vote_count = models.IntegerField(default=0)

    class Meta:
        abstract = True


class GenericModelMixin(models.Model):
    """
    Allows generic relations between different models.
    See https://docs.djangoproject.com/en/2.1/ref/contrib/contenttypes/
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Event(OwnerMixin, CommentMixin, FollowMixin, LocationMixin, MediaMixin, VoteMixin):
    # Related fields
    # TODO Decide if an artist must be a User in our system.
    artists = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='event_artists',
                                     related_name='performed_events')
    tags = models.ManyToManyField('Tag', db_table='event_tags', related_name='events')

    # Own fields
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    organizer_url = models.URLField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class AttendanceStatus(OwnerMixin):
    ATTENDANCE_STATUS = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('M', 'Maybe'),
        ('A', 'Attended'),
        ('B', 'Blocked'),
    )
    event = models.ForeignKey(Event, related_name='attendance_status', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS)

    class Meta:
        # There can be only one attendance status between User and Event.
        unique_together = ('owner', 'event')


class Comment(GenericModelMixin, OwnerMixin):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class FollowStatus(GenericModelMixin, OwnerMixin):
    class Meta:
        # A user cannot follow the same item more than once
        unique_together = ('owner', 'content_type', 'object_id')


class Location(GenericModelMixin, OwnerMixin):
    # TODO Add required fields after doing research about Google Maps / Places API
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # A model (User, Event etc.) cannot have more than one Location.
        unique_together = ('content_type', 'object_id')


class Media(GenericModelMixin, OwnerMixin):
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=20)


class VoteStatus(GenericModelMixin, OwnerMixin):
    VOTE_CHOICES = (
        ('U', 'Up'),
        ('D', 'Down'),
    )
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES)

    class Meta:
        # A user cannot vote for the same item more than once
        unique_together = ('owner', 'content_type', 'object_id')

    @property
    def vote_value(self):
        vote_value = 0
        if self.vote == 'U':
            vote_value = 1
        elif self.vote == 'D':
            vote_value = -1
        return  vote_value
