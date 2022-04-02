from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """
    Default custom user model for main.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class PostNews(models.Model):
    title_news = models.CharField(max_length=128)
    owner_news = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_posts')
    link = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    count_votes = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title_news


class UserCommentPost(models.Model):
    owner_comment = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='my_comments')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    post_news = models.ForeignKey(PostNews, on_delete=models.CASCADE)


class UserVotePost(models.Model):
    post_news = models.ForeignKey(PostNews, on_delete=models.CASCADE)
    owner_vote = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
