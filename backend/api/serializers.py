from rest_framework import serializers

from api.models import Comment, Event, EventMedia, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

# TODO Implement LocationSerializer

class EventMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMedia
        fields = ('id', 'event', 'url')


class CommentSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField

    class Meta:
        model = Comment
        fields = ('id', 'event', 'content', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated')


class EventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'price', 'upvote_count',
                  'downvote_count')


class EventDetailedSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    event_medias = EventMediaSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'price', 'upvote_count',
                  'downvote_count', 'organizer_url', 'tags', 'event_medias', 'comments')
        read_only_fields = ('upvote_count', 'downvote_count')

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        event_medias_data = validated_data.pop('event_medias')
        event = Event(**validated_data)
        event.save()
        for tag_data in tags_data:
            tag_object = Tag.objects.get(id=tag_data['id'])
            if tag_object is not None:
                event.tags.add(tag_data)
        for event_media_data in event_medias_data:
            media_object = EventMedia.objects.create(**event_media_data)
            event.medias.add(media_object)
        return event

    # TODO Implement update
