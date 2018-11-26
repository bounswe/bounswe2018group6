from django.contrib.auth import authenticate, get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.models import (AttendanceStatus, Comment, CorporateUserProfile, Event,
                        FollowStatus, Location, Media, Tag, User, VoteStatus)


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


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


class UserCreateSerializer(serializers.ModelSerializer):
    corporate_profile = CorporateUserSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name',
                  'bio', 'city', 'is_corporate_user', 'corporate_profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        is_corporate_user = validated_data.pop('is_corporate_user', False)
        corporate_profile = validated_data.pop('corporate_profile', None)

        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)

        if None in (username, email, password, first_name, last_name):
            raise serializers.ValidationError('User creation failed due to missing credentials.')

        user = User.objects.create_user(username, email, password)
        user.first_name, user.last_name = first_name, last_name

        user.bio = validated_data.pop('bio', None)
        user.city = validated_data.pop('city', None)
        user.is_corporate_user = is_corporate_user

        if is_corporate_user and corporate_profile is not None:
            corp = CorporateUserProfile.objects.create(**corporate_profile)
            user.corporate_profile = corp
        else:
            user.corporate_profile = None
        user.save()
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    corporate_profile = CorporateUserSerializer()
    tags = TagSerializer(many=True)
    comments = CommentDetailsSerializer(many=True, read_only=True)
    votes = VoteDetailsSerializer(many=True, read_only=True)
    following_count = serializers.SerializerMethodField()
    blocked_users_count = serializers.SerializerMethodField()
    owned_events_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'bio', 'city',
                  'tags', 'comments', 'votes', 'follower_count',
                  'following_count', 'owned_events_count', 'blocked_users_count',
                  'is_corporate_user', 'corporate_profile')
        read_only_fields = ('id', 'username', 'tags', 'comments', 'votes',
                            'follower_count', 'following_count', 'owned_events_count',
                            'blocked_users_count')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.city = validated_data.get('city', instance.city)
        instance.is_corporate_user = validated_data.get('is_corporate_user', instance.is_corporate_user)
        corporate_profile = validated_data.get('corporate_profile', instance.corporate_profile)
        if not instance.is_corporate_user:
            # case: corporate user is disabled
            instance.corporate_profile = None
        else:
            if instance.corporate_profile:
                # case: corporate user profile is updated
                instance.corporate_profile.url = corporate_profile.get('url', None)
            else:
                # case: corporate user profile is enabled with provided data
                corp = CorporateUserProfile.objects.create(url=corporate_profile.get('url', None))
                instance.corporate_profile = corp
            instance.corporate_profile.save()
        instance.save()
        return instance

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
