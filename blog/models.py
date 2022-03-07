from django.db import models
import uuid
from users.models import Profile


# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    body = models.TextField(
        null=True,
        blank=True
    )

    featured_image = models.ImageField(
        null=True,
        blank=True,
        default='default.jpg'
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
        ordering=['-created']