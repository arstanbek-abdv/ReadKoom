from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.users.models import User
# Create your models here.

class Notification(models.Model):

    class EventType(models.TextChoices):
        NEW_FOLLOWER = 'new_follower', 'New Follower' # Someone started following you
        PUBLICATION_RATED = 'publication_rated', 'Publication Rated' # Someone rated your publication
        COMMENTED_PUBLICATION = 'commented_publication', 'Commented Publication' # Someone commented your publication
        COMMENT_LIKED = 'comment_liked','Comment liked' # Someone liked your comment
      
        PUBLICATION_BY_FOLLOWING = 'publication_by_following' ,'Publication by Following' # Someone you follow made a publication
        COMMENT_BY_FOLLOWING = 'comment_by_following','Comment by Following' # Someone you follow made a comment
        
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipients'
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actors'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='entities'
    )
    event_type = models.CharField(max_length=30, choices=EventType.choices)
    object_id = models.PositiveBigIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)