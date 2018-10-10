from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Tag(models.Model):
  name = models.CharField(max_length=10)  # TODO Decide `max_length` with other teams

  class Meta:
    db_table = 'tag'


class Location(models.Model):
  # TODO Implement this after doing research about Google Maps / Places API

  class Meta:
    db_table = 'location'


class Media(models.Model):
  url = models.URLField()

  class Meta:
    db_table = 'media'


class Event(models.Model):
  # Related fields
  artists = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='event_has_artist', related_name='artists')
  tags = models.ManyToManyField(Tag, db_table='event_has_tag', related_name='tags')
  followers = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='event_has_follower', related_name='followers')
  attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='event_has_attendee', related_name='attendees')
  medias = models.ManyToManyField(Media, db_table='event_has_media', related_name='medias')

  # Own fields
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=100)  # TODO Decide `max_length` with other teams
  description = models.TextField()
  date = models.DateTimeField(default=timezone.now)
  location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  upvote_count = models.IntegerField(default=0)
  downvote_count = models.IntegerField(default=0)
  organizer_url = models.URLField()

  class Meta:
    db_table = 'event'


class Comment(models.Model):
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  content = models.TextField()

  class Meta:
    db_table = 'comment'
