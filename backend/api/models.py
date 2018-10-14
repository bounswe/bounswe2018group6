from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Related fields
    interests = models.ManyToManyField('UserInterest', related_name='user_interests')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='user_followers')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='user_followings')
    ratings = models.ManyToManyField('self', symmetrical=False, related_name='user_ratings')
    blocked_users = models.ManyToManyField('self', symmetrical=False, related_name='user_blocked_users')
    owned_events = models.ManyToManyField('Event', related_name='user_owned_events')
    attended_events = models.ManyToManyField('Event', related_name='user_attended_events')
    followed_events = models.ManyToManyField('Event', related_name='user_followed_events')
    blocked_events = models.ManyToManyField('Event', related_name='user_blocked_events')

    # Additional own fields
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    visibility = models.BooleanField(default=True)

    # TODO discuss user rating system to the team.
    user_rating = models.DecimalField(null=True, default=None, max_digits=4, decimal_places=3)
    user_rating_count = models.PositiveIntegerField(default=0)

    # Corporate users have their profiles having their corporate data.
    # Since it's not feasible to create different tables for both
    #   or to use abstract tables
    #   and user groups doesn't meet the requirements due to extra fields in the db
    #   creating another profile is prefered.
    is_corporate_user = models.BooleanField(default=False)
    corporate_profile = models.ForeignKey('CorporateUserProfile', on_delete=models.CASCADE, null=True, default=None)


class CorporateUserProfile(models.Model):
    description = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)


class UserInterest(models.Model):
    name = models.CharField(max_length=50)


class Event(models.Model):
    # TODO This will be merged with another branch of the project.
    pass

class Location(models.Model):
    # TODO Implement this after doing research about Google Maps / Places API
    pass