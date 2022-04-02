from django.db.models.signals import post_save

from django.dispatch import receiver

from .models import PostNews


@receiver(post_save, sender=PostNews)
def signal_create_posts(sender, instance, created, **kwargs):
    if created:
        post = PostNews.objects.get(id=instance.id)
        print(f'Created post {post} - {post.date_created}')
