from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.models import (AttendanceStatus, Comment, CorporateUserProfile, Event,
                        FollowStatus, Location, Media, Tag, User, VoteStatus)


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'profile_photo')

    def search(self, validated_data):
        keyword = validated_data.pop('keyword')


class AttendanceCreateSerializer(serializers.ModelSerializer):
    owner = UserSummarySerializer(read_only=True)

    class Meta:
        model = AttendanceStatus
        fields = ('id', 'owner', 'event', 'status')

    def create(self, validated_data):
        user = self.context.get("request").user
        attendance_status, created = AttendanceStatus.objects.update_or_create(
            owner=user, event=validated_data.pop('event'), defaults={'status':validated_data.pop('status')})
        return attendance_status


class AttendanceDetailsSerializer(serializers.ModelSerializer):
    owner = UserSummarySerializer(read_only=True)

    class Meta:
        model = AttendanceStatus
        fields = ('id', 'owner', 'status')


class CommentCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()
    owner = UserSummarySerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'owner', 'content', 'content_type', 'object_id', 'created', 'updated')

    def create(self, validated_data):
        owner = self.context.get("request").user
        # TODO Validate if content_object exists
        content_object = ContentType.objects.get(model=validated_data.pop('content_type')) \
            .get_object_for_this_type(id=validated_data.pop('object_id'))
        comment = Comment.objects.create(owner=owner, content_object=content_object, **validated_data)
        return comment


class CommentDetailsSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    owner = UserSummarySerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'owner', 'content', 'content_type', 'object_id', 'created', 'updated')
        read_only_fields = ('content_type', 'object_id')

    def get_content_type(self, obj):
        return obj.content_type.model


class FollowCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = FollowStatus
        fields = ('id', 'content_type', 'object_id')

    def create(self, validated_data):
        owner = self.context.get("request").user
        # TODO Validate if content_object exists
        # TODO Validate if content object is already followed by owner
        content_object = ContentType.objects.get(model=validated_data.pop('content_type')) \
            .get_object_for_this_type(id=validated_data.pop('object_id'))
        follow_status = FollowStatus.objects.create(owner=owner, content_object=content_object, **validated_data)
        return follow_status


class FollowDetailsSerializer(serializers.ModelSerializer):
    owner = UserSummarySerializer(read_only=True)

    class Meta:
        model = FollowStatus
        fields = ('id', 'owner')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'city', 'district')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=20, write_only=True)
    token = serializers.CharField(max_length=40, read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Incorrect credentials')

        token, __ = Token.objects.get_or_create(user=user)

        return {
            'token': token,
            'user_id': user.pk,
        }


class MediaCreateSerializer(serializers.ModelSerializer):
    owner = UserSummarySerializer(read_only=True)

    class Meta:
        model = Media
        fields = ('id', 'owner', 'event', 'file', 'created', 'updated')

    def create(self, validated_data):
        owner = self.context.get("request").user
        media = Media.objects.create(owner=owner, **validated_data)
        return media


class MediaDetailsSerializer(serializers.ModelSerializer):
    owner = UserSummarySerializer(read_only=True)

    class Meta:
        model = Media
        fields = ('id', 'owner', 'event', 'file', 'created', 'updated')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class VoteCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = VoteStatus
        fields = ('id', 'content_type', 'object_id', 'vote')

    def create(self, validated_data):
        owner = self.context.get("request").user
        # TODO Validate if content_object exists
        content_type_object = ContentType.objects.get(model=validated_data['content_type'])
        content_object = content_type_object.get_object_for_this_type(id=validated_data['object_id'])
        vote_status, created = VoteStatus.objects.get_or_create(
            owner=owner, content_type=content_type_object, object_id=validated_data['object_id'],
            defaults={'vote': validated_data['vote']})
        if created:
            content_object.update_vote_count(vote_status.vote_value, False)
        else:
            if vote_status.vote == validated_data['vote']:
                raise serializers.ValidationError('Cannot vote for the item with the same vote value.')
            else:
                vote_status.vote = validated_data['vote']
                vote_status.save()
                content_object.update_vote_count(vote_status.vote_value, True)
        return vote_status


class VoteDetailsSerializer(serializers.ModelSerializer):
    owner = UserSummarySerializer(read_only=True)

    class Meta:
        model = VoteStatus
        fields = ('id', 'owner', 'vote')


class CorporateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorporateUserProfile
        fields = ('url',)


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    corporate_profile = CorporateUserSerializer(required=False, allow_null=True)
    current_password = serializers.CharField(min_length=8, max_length=20, trim_whitespace=False, 
                                                write_only=True, required=False)
    new_password = serializers.CharField(min_length=8, max_length=20, trim_whitespace=False, 
                                                write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'current_password', 'new_password',
                  'first_name', 'last_name', 'profile_photo', 'bio', 'city', 
                  'is_corporate_user', 'corporate_profile', 'tags')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8, 'max_length': 20}}

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)

        user = User.objects.create_user(username, email, password)

        is_corporate_user = validated_data.pop('is_corporate_user', False)
        corporate_profile = validated_data.pop('corporate_profile', None)
        
        user.is_corporate_user = is_corporate_user
        if is_corporate_user and corporate_profile is not None:
            corp = CorporateUserProfile.objects.create(**corporate_profile)
            user.corporate_profile = corp
        else:
            user.corporate_profile = None
        
        for key, value in validated_data.items():
            setattr(user, key, value)

        user.save()
        return user

    def update(self, instance, validated_data):
        # username can't be changed, yet email can be
        username = validated_data.pop('username', None)
        if username is not None and username != instance.username:
            raise serializers.ValidationError('Username can\'t be changed.')

        # password change
        new_password = validated_data.pop('new_password', None)
        if new_password:
            current_password = validated_data.pop('current_password', None)
            if check_password(current_password, instance.password):
                instance.set_password(new_password)
            else:
                serializers.ValidationError('Current password is wrong.')

        # corporate user profile handling
        instance.is_corporate_user = validated_data.pop('is_corporate_user', instance.is_corporate_user)
        corporate_profile = validated_data.pop('corporate_profile', instance.corporate_profile)
        if not instance.is_corporate_user:
            # case: corporate user is disabled
            instance.corporate_profile = None
        else:
            if instance.corporate_profile:
                # case: corporate user profile is updated
                for key, value in corporate_profile.items():
                    setattr(instance.corporate_profile, key, value)
                instance.corporate_profile.save()
            else:
                # case: corporate user profile is enabled with provided data
                corp = CorporateUserProfile.objects.create(**corporate_profile)
                instance.corporate_profile = corp
        
        # tags handling
        # If 'tags' key is given in data, clear current tags and add new ones.
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.clear()
            for tag in tags_data:
                instance.tags.add(tag)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class UserDetailsSerializer(serializers.ModelSerializer):
    corporate_profile = CorporateUserSerializer()
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentDetailsSerializer(many=True, read_only=True)
    votes = VoteDetailsSerializer(many=True, read_only=True)
    following_count = serializers.SerializerMethodField()
    blocked_users_count = serializers.SerializerMethodField()
    owned_events_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'profile_photo', 'bio', 'city',
                  'tags', 'comments', 'votes', 'follower_count',
                  'following_count', 'owned_events_count', 'blocked_users_count',
                  'is_corporate_user', 'corporate_profile')

    def get_following_count(self, obj):
        return FollowStatus.objects.filter(owner=obj).count()

    def get_blocked_users_count(self, obj):
        return obj.blocked_users.count()

    def get_owned_events_count(self, obj):
        return obj.event_set.count()


class EventSummarySerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    own_attendance_status = serializers.SerializerMethodField()
    own_follow_status = serializers.SerializerMethodField()
    own_vote = serializers.SerializerMethodField()
    owner = UserSummarySerializer()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'owner', 'featured_image', 'title', 'description', 'date', 'price',
                  'location', 'created', 'updated', 'own_attendance_status', 'follower_count',
                  'own_follow_status', 'vote_count', 'own_vote', 'tags')

    def get_own_attendance_status(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_attendance = obj.attendance_status.all().filter(owner=user).first()
            return {'id': own_attendance.id, 'status': own_attendance.status} if own_attendance else None
        return None

    def get_own_follow_status(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_follow = obj.followers.all().filter(owner=user).first()
            return {'id': own_follow.id} if own_follow else None
        return None

    def get_own_vote(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_vote = obj.votes.all().filter(owner=user).first()
            return {'id': own_vote.id, 'vote': own_vote.vote} if own_vote else None
        return None

    def search(self, validated_data):
        keyword = validated_data.pop('keyword')


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    owner = UserSummarySerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'owner', 'featured_image', 'title', 'description', 'date', 'price',
                  'created', 'updated', 'organizer_url', 'artists', 'location', 'tags')

    def create(self, validated_data):
        # Required fields
        owner = self.context.get("request").user
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)

        # Optional fields
        artists_data = validated_data.pop('artists', [])
        tags_data = validated_data.pop('tags', [])
        event = Event.objects.create(owner=owner, location=location, **validated_data)
        for artist in artists_data:
            event.artists.add(artist)
        for tag in tags_data:
            event.tags.add(tag)
        return event

    def update(self, instance, validated_data):
        owner = self.context.get("request").user

        # If 'artists' key is given in data, clear current artists
        # and add new ones. Else, discard it.
        if 'artists' in validated_data:
            artists_data = validated_data.pop('artists')
            instance.artists.clear()
            for artist in artists_data:
                instance.artists.add(artist)

        # If 'location' key is given in data, delete current location
        # and create a new one. Else, discard it.
        if 'location' in validated_data:
            location_data = validated_data.pop('location')
            instance.location.delete()
            instance.location = Location.objects.create(**location_data)

        # If 'tags' key is given in data, clear current tags
        # and add new ones. Else, discard it.
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.clear()
            for tag in tags_data:
                instance.tags.add(tag)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class EventDetailsSerializer(serializers.ModelSerializer):
    artists = UserSummarySerializer(many=True, read_only=True)
    attendance_status = AttendanceDetailsSerializer(many=True, read_only=True)
    comments = CommentDetailsSerializer(many=True, read_only=True)
    followers = FollowDetailsSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)
    medias = MediaDetailsSerializer(many=True, read_only=True)
    own_attendance_status = serializers.SerializerMethodField()
    own_follow_status = serializers.SerializerMethodField()
    own_vote = serializers.SerializerMethodField()
    owner = UserSummarySerializer()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'owner', 'featured_image', 'title', 'description', 'date', 'price', 'location', 'organizer_url',
                  'created', 'updated', 'artists', 'attendance_status', 'own_attendance_status',
                  'comments', 'followers', 'follower_count', 'own_follow_status', 'medias',
                  'tags', 'vote_count', 'own_vote')

    def get_own_attendance_status(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_attendance = obj.attendance_status.all().filter(owner=user).first()
            return {'id': own_attendance.id, 'status': own_attendance.status} if own_attendance else None
        return None

    def get_own_follow_status(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_follow = obj.followers.all().filter(owner=user).first()
            return {'id': own_follow.id} if own_follow else None
        return None

    def get_own_vote(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_vote = obj.votes.all().filter(owner=user).first()
            return {'id': own_vote.id, 'vote': own_vote.vote} if own_vote else None
        return None
