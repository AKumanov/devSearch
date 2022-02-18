from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User 
from users.models import Profile



def create_profile(sender, instance, created, **kwargs):
    """
    when you create a new user, automatically a new profile, tied to the user is created
    sender - the model, that sends the signal
    instance - the instance of the model, that triggers this (object)
    created - boolean
    """
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email=user.email,
            name=user.first_name,
        )


def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(create_profile, sender=User)
post_delete.connect(delete_user, sender=Profile)