from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from api.models import AttendanceStatus, Comment, Event, FollowStatus, Media, Tag


class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceStatus
        fields = ('id', 'event', 'status')

    def create(self, validated_data):
        user = self.context.get("request").user
        attendance_status, created = AttendanceStatus.objects.update_or_create(
            user=user, event=validated_data['event'], defaults={'status':validated_data['status']})
        return attendance_status


class AttendanceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceStatus
        fields = ('id', 'user', 'event', 'status')
        read_only_fields = ('id', 'user', 'status')


class CommentCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'content_type', 'object_id')

    def create(self, validated_data):
        owner = self.context.get("request").user
        content_object = ContentType.objects.get(model=validated_data.pop('content_type')) \
            .get_object_for_this_type(id=validated_data.pop('object_id'))
        comment = Comment.objects.create(owner=owner, content_object=content_object, **validated_data)
        return comment


class CommentDetailsSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'owner', 'content_type', 'object_id', 'content', 'created', 'updated')
        read_only_fields = ('owner', 'content_type', 'object_id', 'created', 'updated')

    def get_content_type(self, obj):
        return obj.content_type.model


class FollowCreateDeleteSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = FollowStatus
        fields = ('id', 'content_type', 'object_id')

    def create(self, validated_data):
        owner = self.context.get("request").user
        content_object = ContentType.objects.get(model=validated_data.pop('content_type')) \
            .get_object_for_this_type(id=validated_data.pop('object_id'))
        follow_status = FollowStatus.objects.create(owner=owner, content_object=content_object, **validated_data)
        return follow_status


class FollowDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowStatus
        fields = ('id', 'owner')
        read_only_fields = ('id', 'owner')


class MediaCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = Media
        fields = ('id', 'url', 'content_type', 'object_id')

    def create(self, validated_data):
        owner = self.context.get("request").user
        content_object = ContentType.objects.get(model=validated_data.pop('content_type')) \
            .get_object_for_this_type(id=validated_data.pop('object_id'))
        media = Media.objects.create(owner=owner, content_object=content_object, **validated_data)
        return media


class MediaDetailsSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ('id', 'owner', 'content_type', 'object_id', 'url', 'created', 'updated')

    def get_content_type(self, obj):
        return obj.content_type.model


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class EventSummarySerializer(serializers.ModelSerializer):
    own_attendance_status = serializers.SerializerMethodField()
    own_follow_status = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'owner', 'title', 'description', 'date', 'price',
                  'created', 'updated', 'own_attendance_status', 'follower_count',
                  'own_follow_status')

    def get_own_attendance_status(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_attendance = obj.attendance_status.all().filter(user=user).first()
            return '' if own_attendance is None else own_attendance.status
        return ''

    def get_own_follow_status(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_follow = obj.followers.all().filter(owner=user).first()
            return 'N' if own_follow is None else 'Y'
        return ''


class EventCreateSerializer(serializers.ModelSerializer):
    medias = MediaCreateSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'price', 'organizer_url', 'medias', 'tags')

    # TODO Fix problems
    # def create(self, validated_data):
    #     owner = self.context.get("request").user
    #     medias_data = validated_data.pop('medias')
    #     tags_data = validated_data.pop('tags')
    #     event = Event.objects.create(owner=owner, **validated_data)
    #     for media_data in medias_data:
    #         Media.objects.create(content_object=event, url=media_data['url'])
    #     for tag_data in tags_data:
    #         tag_object = Tag.objects.get(id=tag_data['id'])
    #         if tag_object is not None:
    #             event.tags.add(tag_object)
    #     return event


class EventDetailsSerializer(serializers.ModelSerializer):
    attendance_status = AttendanceDetailsSerializer(many=True, read_only=True)
    own_attendance_status = serializers.SerializerMethodField()
    comments = CommentDetailsSerializer(many=True, read_only=True)
    followers = FollowDetailsSerializer(many=True, read_only=True)
    own_follow_status = serializers.SerializerMethodField()
    medias = MediaDetailsSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'owner', 'title', 'description', 'date', 'price', 'organizer_url', 'created', 'updated',
                  'attendance_status', 'own_attendance_status', 'comments', 'followers', 'follower_count',
                  'own_follow_status', 'medias', 'tags')
        read_only_fields = ('owner', 'created', 'updated')

    def get_own_attendance_status(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_attendance = obj.attendance_status.all().filter(user=user).first()
            return '' if own_attendance is None else own_attendance.status
        return ''

    def get_own_follow_status(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            own_follow = obj.followers.all().filter(owner=user).first()
            return 'N' if own_follow is None else 'Y'
        return ''

    # TODO Fix problems
    # def update(self, instance, validated_data):
    #     medias_data = validated_data.pop('medias')
    #     tags_data = validated_data.pop('tags')
    #     Event.objects.filter(id=instance.id).update(**validated_data)
    #     if (len(medias_data) != 0):
    #         instance.medias.all().delete()
    #         for media_data in medias_data:
    #             media_object = Media.objects.create(content_object=event, url=media_data['url'])
    #     if (len(tags_data) != 0):
    #         instance.tags.clear()
    #         for tag_data in tags_data:
    #             print(tag_data)
    #             tag_object = Tag.objects.get(id=tag_data['id'])
    #             if tag_object is not None:
    #                 instance.tags.add(tag_object)
    #     return instance
