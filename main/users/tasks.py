from django.contrib.auth import get_user_model
import logging
from config import celery_app
from quick_publisher.celery import app
# from main.config.celery_app import app
from .models import PostNews
import datetime

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@app.task
def update_count_vote(post_id):
    try:
        post = PostNews.objects.get(pk=post_id)
        today = datetime.datetime.now(datetime.timezone.utc)
        if post.count_votes != today:
            post.count_votes = 0
            post.save()
    except PostNews.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % post_id)


