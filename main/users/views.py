import datetime

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import PostNews, UserCommentPost, UserVotePost
from .serializers import (
    PostNewsSerializer,
    RegisterSerializer,
    UserCommentPostSerializer,
    UserSerializer,
    UserVotePostSerializer,
)

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegisterUserApi(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostCreateViewSet(ModelViewSet):
    queryset = PostNews.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = PostNewsSerializer

    def perform_create(self, serializer):
        serializer.validated_data['owner_news'] = self.request.user
        serializer.save()


class PostCreateCommentViewSet(ModelViewSet):
    queryset = UserCommentPost.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserCommentPostSerializer

    def perform_create(self, serializer):
        serializer.validated_data['owner_comment'] = self.request.user
        serializer.save()


class UserVotePostViewSet(ModelViewSet):
    queryset = UserVotePost.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = UserVotePostSerializer

    def perform_create(self, serializer):
        serializer.validated_data['owner_vote'] = self.request.user
        serializer.save()


def update_count_post(request, pk):
    try:
        post = PostNews.objects.get(pk=pk)

    except:
        raise Http404("Post does not exist")

    post.count_votes = 0
    post.save()
    # today = datetime.datetime.now(timezone.utc)
    # if post.count_votes > 0:
    #     post.count_votes = 0
    #     post.save()

    return redirect('users/api_app/post_create')
