from rest_framework import generics, mixins, views, status
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.models import (AttendanceStatus, Comment, CorporateUserProfile, Event,
                        FollowStatus, Media, Tag, User, VoteStatus)
from api.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from api.serializers import (AttendanceCreateSerializer,
                             CommentCreateSerializer, CommentDetailsSerializer,
                             EventCreateUpdateSerializer,
                             EventDetailsSerializer, EventSummarySerializer,
                             LoginSerializer, FollowCreateSerializer, MediaCreateSerializer,
                             MediaDetailsSerializer, TagSerializer,
                             UserCreateSerializer, UserDetailsSerializer,
                             VoteCreateSerializer)


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


class LoginView(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaView(generics.RetrieveAPIView,
                generics.CreateAPIView,
                generics.DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class SignUpView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserView(generics.RetrieveAPIView,
               mixins.UpdateModelMixin):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsUserOrReadOnly)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class VoteView(generics.CreateAPIView,
               generics.DestroyAPIView):
    queryset = VoteStatus.objects.all()
    serializer_class = VoteCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
