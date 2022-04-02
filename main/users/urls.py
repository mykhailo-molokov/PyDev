from django.urls import path, include

from .views import PostCreateCommentViewSet, UserVotePostViewSet, PostCreateViewSet, RegisterUserApi, update_count_post

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('post_create', PostCreateViewSet)
router.register('comment_create', PostCreateCommentViewSet)
router.register('vote_create', UserVotePostViewSet)

app_name = "users"
urlpatterns = [
    path('reg/', RegisterUserApi.as_view(), name='register_user'),
    path('update/<int:pk>/', update_count_post, name='update'),
    path('api_app/', include(router.urls)),
]
