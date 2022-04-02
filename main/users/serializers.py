from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import PostNews, UserCommentPost, UserVotePost

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserCommentPostSerializer(serializers.ModelSerializer):
    owner_comment = serializers.CharField(source='owner_comment.username', default='', read_only=True)

    class Meta:
        model = UserCommentPost
        fields = ('owner_comment', 'content', 'date_created', 'post_news')


class UserVotePostSerializer(serializers.ModelSerializer):
    owner_vote = serializers.CharField(source='owner_vote.username', default='', read_only=True)

    class Meta:
        model = UserVotePost
        fields = ('post_news', 'owner_vote', 'like')


class PostNewsSerializer(serializers.ModelSerializer):
    owner_news = serializers.CharField(source='owner_news.username', default='', read_only=True)
    count_votes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostNews
        fields = ('title_news', 'owner_news', 'link', 'date_created', 'count_votes')

    def get_count_votes(self, instance):

        return UserVotePost.objects.filter(post_news=instance, like=True).count()
