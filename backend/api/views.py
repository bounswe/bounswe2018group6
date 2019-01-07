"""
.. module:: views
   :platform: Unix, Windows
   :synopsis: Views

"""
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from notifications.models import Notification, NotificationQuerySet
from rest_framework import filters, generics, mixins, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.models import (Annotation, AttendanceStatus, Comment, Conversation,
                        CorporateUserProfile, Event, FollowStatus, Media,
                        Message, ShareStatus, Tag, User, VoteStatus)
from api.permissions import (IsOwnerOrParticipant, IsOwnerOrReadOnly,
                             IsUserOrReadOnly)
from api.serializers import (AnnotationCreate, AnnotationDetailsSerializer,
                             AttendanceCreateSerializer,
                             CommentCreateSerializer, CommentDetailsSerializer,
                             ConversationCreateSerializer,
                             ConversationSerializer,
                             EventCreateUpdateSerializer,
                             EventDetailsSerializer, EventSummarySerializer,
                             FollowCreateSerializer, LoginSerializer,
                             MediaCreateSerializer, MediaDetailsSerializer,
                             MessageCreateSerializer, ShareCreateSerializer,
                             TagSerializer, UserCreateUpdateSerializer,
                             UserDetailsSerializer, UserSummarySerializer,
                             VoteCreateSerializer)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_notifications_list(request):
    """
    :param request: request for notifications   
    :returns: all notifications data with id, data, timestamp in json data
    """
    all_list = []
    for notification in request.user.notifications.all():
        all_list.append({
            "id": notification.id,
            "data": notification.verb,
            "timestamp": notification.timestamp
        })
    data = {
        'count': request.user.notifications.all().count(),
        'notifications': all_list
    }
    return JsonResponse(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_notifications_list(request):
    """
    :param request: request for notifications   
    :returns: only unreaded notifications data with id, data, timestamp in json data
    """
    unread_list = []
    for notification in request.user.notifications.unread():
        unread_list.append({
            "id": notification.id,
            "data": notification.verb,
            "timestamp": notification.timestamp
        })
    data = {
        'count': request.user.notifications.unread().count(),
        'notifications': unread_list
    }
    return JsonResponse(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    """
    :param request: request for notifications   
    :returns: marks all notifications read and returns success
    """
    request.user.notifications.mark_all_as_read()
    return HttpResponse(status=200)

class MultiSerializerViewMixin(object):

    def get_serializer_class(self):
        """
        :param self: self object
        :returns: serializers class
        """
        try:
            return self.method_serializer_classes[self.request.method]
        except:
            return super(MultiSerializerViewMixin, self).get_serializer_class()


class AnnotationView(MultiSerializerViewMixin,
                     generics.RetrieveAPIView,
                     generics.CreateAPIView,
                     generics.DestroyAPIView,
                     mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Annotation.objects.all()
    serializer_class = AnnotationDetailsSerializer
    method_serializer_classes = {
        'POST': AnnotationCreate,
    }

    def put(self, request, *args, **kwargs):
        """
        :param self: self object
        :param request: request object
        :param *args: args
        :param **kwargs: **kwargs 
        :returns: annotations of image
        """
        return self.partial_update(request, *args, **kwargs)


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
        """
        :param self: self object
        :param request: request object
        :param *args: args
        :param **kwargs: **kwargs 
        :returns: comment
        """
        return self.partial_update(request, *args, **kwargs)


class ConversationListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects. \
            filter(Q(owner=self.request.user) | Q(participant=self.request.user)).order_by('-updated')


class ConversationView(MultiSerializerViewMixin,
                       generics.RetrieveAPIView,
                       generics.CreateAPIView,
                       generics.DestroyAPIView):
    queryset = Conversation.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrParticipant)
    serializer_class = ConversationSerializer
    method_serializer_classes = {
        'POST': ConversationCreateSerializer,
    }


class EventRecommendedListView(generics.ListAPIView):
    serializer_class = EventSummarySerializer

    def get_queryset(self):
        """
        :param self: self object
        :returns: recomended events for the user
        """
        return sorted(Event.objects.annotate(num_tags=Count('tags')).filter(num_tags__gt=0), reverse=True, key=lambda x: sum(tag in x.tags.all() for tag in self.request.user.tags.all()))


class EventListView(generics.ListAPIView):
    """
        Creates events list as searchable according title and description fields
    """
    queryset = Event.objects.all()
    serializer_class = EventSummarySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title','description')


class EventLocationSearchView(generics.ListAPIView):
    """
        Creates events list as searchable according city and disrtrict fields
    """
    queryset = Event.objects.all()
    serializer_class = EventSummarySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('location__city','location__district')


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
        """
        :param self: self object
        :param request: request object
        :param *args: args
        :param **kwargs: **kwargs 
        :returns: an event
        """
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
        """
        :param self: self object
        :param request: request object
        :param *args: args
        :param **kwargs: **kwargs 
        :returns: response of login
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaView(generics.RetrieveAPIView,
                generics.CreateAPIView,
                generics.DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class MessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageCreateSerializer


class ShareView(generics.CreateAPIView,
                generics.DestroyAPIView):
    queryset = ShareStatus.objects.all()
    serializer_class = ShareCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class SignUpView(generics.CreateAPIView):
    serializer_class = UserCreateUpdateSerializer
    permission_classes = (AllowAny,)


class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserView(MultiSerializerViewMixin,
               generics.RetrieveAPIView,
               mixins.UpdateModelMixin):
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsAuthenticatedOrReadOnly, IsUserOrReadOnly)
    serializer_class = UserDetailsSerializer
    method_serializer_classes = {
        'POST': UserCreateUpdateSerializer,
        'PUT': UserCreateUpdateSerializer,
    }

    def put(self, request, *args, **kwargs):
        """
        :param self: self object
        :param request: request object
        :param *args: args
        :param **kwargs: **kwargs 
        :returns: a user
        """
        return self.partial_update(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSummarySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username','first_name','last_name')


class VoteView(generics.CreateAPIView,
               generics.DestroyAPIView):
    queryset = VoteStatus.objects.all()
    serializer_class = VoteCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
