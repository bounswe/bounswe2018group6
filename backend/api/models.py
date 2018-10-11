from django.db import models
from django.conf import settings
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=10)  # TODO Decide `max_length` with other teams

    class Meta:
        db_table = 'tag'


class Event(models.Model):
    # Related fields
    artists = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='event_has_artist',
                                     related_name='artists')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='event_has_follower',
                                       related_name='followers')
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='event_has_attendee',
                                       related_name='attendees')
    tags = models.ManyToManyField(Tag, db_table='event_has_tag', related_name='tags')

    # Own fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)  # TODO Decide `max_length` with other teams
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    organizer_url = models.URLField(null=True)

    class Meta:
        db_table = 'event'


class Media(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField()

    class Meta:
        abstract = True


class EventMedia(Media):
    event = models.ForeignKey(Event, related_name='event_medias', on_delete=models.CASCADE)

    class Meta:
        db_table = 'event_media'


class Comment(models.Model):
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        db_table = 'comment'


class Location(models.Model):
    # TODO Implement this after doing research about Google Maps / Places API

    class Meta:
        abstract = True
