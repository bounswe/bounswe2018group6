from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (User as CustomUser, CorporateUserProfile, Event, AttendanceStatus,
                     Comment, FollowStatus, Location, Media, Tag, VoteStatus)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    '''
    # manual model display
    fields = ('id', 
              ('is_active', 'is_superuser'),
              ('is_staff', 'is_corporate_user'), 
              ('last_login', 'date_joined'),
              'username', 'email', ('first_name', 'last_name'), 
              'bio', 'city', 'corporate_profile', 
              'follower_count', 'vote_count')
    fieldsets = None
    '''
    # imported from django.contrib.admin.models
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name',
                                      'bio', 'city', 'follower_count', 'vote_count')}),
        ('Corporate User', {'fields': ('is_corporate_user', 'corporate_profile')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('id', 'last_login', 'date_joined', 'follower_count', 'vote_count')

    ordering = ('-id',)
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'is_corporate_user', 'follower_count', 'vote_count')
    list_editable = ('first_name', 'last_name')
    list_filter = ('is_active', 'is_superuser', 'is_staff', 'is_corporate_user', 'city')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('id', 'featured_image',
              'title', 'description', 'date', 'price', 
              'owner', 'organizer_url', 'location', 
              'follower_count', 'vote_count',
              'created', 'updated')
    readonly_fields = ('id', 'follower_count', 'vote_count', 'created', 'updated')
    date_hierarchy = 'date'

    ordering = ('-id')
    list_display = ('id', 'title', 'date', 'price', 
                    'owner', 'organizer_url', 'location', 
                    'follower_count', 'vote_count')
    list_editable = ('title', 'date', 'price')
    list_filter = ('date', 'owner', 'location')
    
    save_on_top = True
