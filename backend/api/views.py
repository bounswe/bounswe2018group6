from rest_framework import generics, mixins
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.models import (AttendanceStatus, Comment, Event, FollowStatus, Media,
                        Tag)
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (AttendanceCreateDestroySerializer,
                             CommentCreateSerializer, CommentDetailsSerializer,
                             EventCreateSerializer, EventDetailsSerializer,
                             EventSummarySerializer,
                             FollowCreateDeleteSerializer,
                             MediaCreateSerializer, MediaDetailsSerializer,
                             TagSerializer)


class MultiSerializerViewMixin(object):

    def get_serializer_class(self):
        try:
            return self.method_serializer_classes[self.request.method]
        except:
            return super(MultiSerializerViewMixin, self).get_serializer_class()


class AttendanceCreateDestroyView(mixins.CreateModelMixin,
                                  mixins.DestroyModelMixin,
                                  generics.GenericAPIView):
    queryset = AttendanceStatus.objects.all()
    serializer_class = AttendanceCreateDestroySerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentView(MultiSerializerViewMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentDetailsSerializer
    method_serializer_classes = {
        'POST': CommentCreateSerializer,
    }

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EventListView(mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSummarySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventView(MultiSerializerViewMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Event.objects.all()
    serializer_class = EventDetailsSerializer
    method_serializer_classes = {
        'POST': EventCreateSerializer,
    }

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class FollowView(mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = FollowStatus.objects.all()
    serializer_class = FollowCreateDeleteSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MediaView(mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TagList(mixins.ListModelMixin,
              generics.GenericAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
