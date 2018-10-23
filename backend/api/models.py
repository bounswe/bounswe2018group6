from django.conf import settings
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class Event(models.Model):
    # Related fields
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_events', on_delete=models.CASCADE)
    # TODO Decide if an artist must be a User in our system.
    artists = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='event_artists',
                                     related_name='performed_events')
    comments = GenericRelation('Comment')
    location = GenericRelation('Location')
    medias = GenericRelation('Media')
    tags = models.ManyToManyField('Tag', db_table='event_tags', related_name='events')

    # Own fields
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    organizer_url = models.URLField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Location(models.Model):
    """
    Different models (User, Event etc.) may need Location, so it's implemented
    according to `contenttypes` framework in order to be a generic model.
    (https://docs.djangoproject.com/en/2.1/ref/contrib/contenttypes/)
    """

    # Related fields
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Own Fields
    # TODO Add required fields after doing research about Google Maps / Places API
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # A model (User, Event etc.) cannot have more than one Location.
        unique_together = ('content_type', 'object_id')


class Media(models.Model):
    """
    Different models (User, Event etc.) may need Media, so it's implemented
    according to `contenttypes` framework in order to be a generic model.
    (https://docs.djangoproject.com/en/2.1/ref/contrib/contenttypes/)
    """

    # Related fields
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='medias', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Own fields
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    """
    Different models (User, Event etc.) may need Location, so it's implemented
    according to `contenttypes` framework in order to be a generic model.
    (https://docs.djangoproject.com/en/2.1/ref/contrib/contenttypes/)
    """

    # Related fields
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Own fields
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class AttendanceStatus(models.Model):
    ATTENDANCE_STATUS = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('M', 'Maybe'),
        ('A', 'Attended'),
        ('B', 'Blocked'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attendance_status', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='attendance_status', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS)

    class Meta:
        # There can be only one attendance status between User and Event.
        unique_together = ('user', 'event')


class Tag(models.Model):
    name = models.CharField(max_length=20)
