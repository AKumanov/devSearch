from django.db import models
import uuid
from users.models import Profile
from ckeditor_uploader.fields import RichTextUploadingField


class Topic(models.Model):
    title = models.CharField(
        max_length=250,
    )

    description = models.TextField(

    )

    image = models.ImageField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    body = RichTextUploadingField(
        null=True,
        blank=True
    )

    featured_image = models.ImageField(
        null=True,
        blank=True,
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )

    is_featured = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
