from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (User as CustomUser, CorporateUserProfile, Event, AttendanceStatus,
                     Comment, FollowStatus, Location, Media, Tag, VoteStatus)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # partially imported from django.contrib.admin.models
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('profile_photo', 'email', 'first_name', 'last_name',
                                      'bio', 'city', 'tags', 'follower_count', 'vote_count')}),
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

    ordering = ('-id',)
    list_display = ('id', 'title', 'date', 'price', 
                    'owner', 'organizer_url', 'location', 
                    'follower_count', 'vote_count')
    list_editable = ('title', 'date', 'price')
    list_filter = ('date', 'owner', 'location')
    
    save_on_top = True


@admin.register(CorporateUserProfile)
class CorporateUserProfileAdmin(admin.ModelAdmin):
    fields = ('id', 'url')
    readonly_fields = ('id',)

    ordering = ('-id',)
    list_display = ('id', 'url')
    list_editable = ('url',)


@admin.register(AttendanceStatus)
class AttendanceStatusAdmin(admin.ModelAdmin):
    fields = ('id', 'event', 'owner', 'status')
    readonly_fields = ('id', 'owner', 'event')

    ordering = ('event', 'owner')
    list_display = ('event', 'owner', 'status')
    list_editable = ('status',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    # TODO Add required fields after completing the model
    fields = ('id', 'city', 'district')
    readonly_fields = ('id',)

    ordering = ('city', 'district')
    list_display = ('id', 'city', 'district')
    list_editable = ('city', 'district')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    fields = ('id', 'owner', 'event', 'file', 'created', 'updated')
    readonly_fields = ('id', 'created', 'updated')

    ordering = ('-id',)
    list_display = ('id', 'owner', 'event', 'file', 'created', 'updated')
    list_editable = ('owner', 'event')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('id', 'name')
    readonly_fields = ('id',)

    ordering = ('name',)
    list_display = ('id', 'name')
    list_editable = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('id', 'object_id', 'content_type_id', 'owner_id',
              'content', 'created', 'updated')
    readonly_fields = ('id', 'object_id', 'content_type_id', 'owner_id',
                       'created', 'updated')

    ordering = ('-created', '-id')
    list_display = ('id', 'object_id', 'content_type_id', 'owner_id',
                    'content', 'created', 'updated')
    list_editable = ('content',)


@admin.register(FollowStatus)
class FollowStatusAdmin(admin.ModelAdmin):
    fields = ('id', 'object_id', 'content_type_id', 'owner_id')
    readonly_fields = ('id', 'object_id', 'content_type_id', 'owner_id')

    ordering = ('id',)
    list_display = ('id', 'object_id', 'content_type_id', 'owner_id')


@admin.register(VoteStatus)
class VoteStatusAdmin(admin.ModelAdmin):
    fields = ('id', 'object_id', 'content_type_id', 'owner_id', 'vote')
    readonly_fields = ('id', 'object_id', 'content_type_id', 'owner_id')

    ordering = ('id',)
    list_display = ('id', 'object_id', 'content_type_id', 'owner_id', 'vote')
    list_editable = ('vote',)
