from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.users.models import User
# Create your models here.

class Publication (models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True,blank=True)
    langauge = models.CharField(max_length=20)
    # R2 reference 
    file_key = models.CharField(max_length=512)
    file_name = models.CharField(max_length=255)        
    file_size = models.PositiveBigIntegerField()     
    mime_type = models.CharField(max_length=127)       
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='post_owner'
    )
    # Status — important for presigned URL flow
    upload_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    favorite_publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name='favorite_publications'
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
   
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','favorite_publication'],
                name='unique_favorite'
            )
        ]


class Rating(models.Model):
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='reviewers'
    )
    publication = models.ForeignKey(
        Publication,
        on_delete=models.PROTECT,
        related_name='reviewed_publications'
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['score','user'],
                name='unique_score_user'
            )
        ]


class Comment(models.Model):
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='commentators'
    )
    publication = models.ForeignKey(
        Publication,
        on_delete=models.PROTECT,
        related_name='commented_publications'
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

