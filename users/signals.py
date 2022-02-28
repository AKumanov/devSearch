from re import sub
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

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

        subject = f'Hello {user.username}, Welcome to DevSearch'
        message = 'We are glad you are here!'
        # send emails when user registers an accounts
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(create_profile, sender=User)
post_delete.connect(delete_user, sender=Profile)
post_save.connect(update_user, sender=Profile)