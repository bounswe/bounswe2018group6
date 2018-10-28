from rest_framework import generics, mixins
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.models import (AttendanceStatus, Comment, Event, FollowStatus, Media,
                        Tag, VoteStatus)
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (AttendanceCreateSerializer,
                             CommentCreateSerializer, CommentDetailsSerializer,
                             EventCreateUpdateSerializer, EventDetailsSerializer,
                             EventSummarySerializer,
                             FollowCreateSerializer,
                             MediaCreateSerializer, MediaDetailsSerializer,
                             TagSerializer, VoteCreateSerializer)


class MultiSerializerViewMixin(object):

    def get_serializer_class(self):
        try:
            return self.method_serializer_classes[self.request.method]
        except:
            return super(MultiSerializerViewMixin, self).get_serializer_class()


class AttendanceView(generics.CreateAPIView,
                     generics.DestroyAPIView):
    queryset = AttendanceStatus.objects.all()
    serializer_class = AttendanceCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class CommentView(MultiSerializerViewMixin,
                  generics.RetrieveAPIView,
                  generics.CreateAPIView,
                  generics.DestroyAPIView,
                  mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Comment.objects.all()
    serializer_class = CommentDetailsSerializer
    method_serializer_classes = {
        'POST': CommentCreateSerializer,
    }

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSummarySerializer


class EventView(MultiSerializerViewMixin,
                generics.RetrieveAPIView,
                generics.CreateAPIView,
                generics.DestroyAPIView,
                mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Event.objects.all()
    serializer_class = EventDetailsSerializer
    method_serializer_classes = {
        'POST': EventCreateUpdateSerializer,
        'PUT': EventCreateUpdateSerializer,
    }

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class FollowView(generics.CreateAPIView,
                 generics.DestroyAPIView):
    queryset = FollowStatus.objects.all()
    serializer_class = FollowCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class MediaView(generics.RetrieveAPIView,
                generics.CreateAPIView,
                generics.DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class VoteView(generics.CreateAPIView,
               generics.DestroyAPIView):
    queryset = VoteStatus.objects.all()
    serializer_class = VoteCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
