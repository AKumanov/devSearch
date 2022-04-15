from django.contrib.auth.models import User
from django.test import TestCase
from users.models import Profile


class TestSignals(TestCase):
    USER_DATA = {
        'username': 'kumana',
        'email': 'kumana@abv.bg',
        'password': 'SomeRan902Pas',
    }

    def __create_user_and_profile(self):
        user = User(**self.USER_DATA)
        user.save()
        profile = Profile.objects.first()

        return user, profile

    def test_create_profile_when_user_is_created(self):
        user, profile = self.__create_user_and_profile()

        self.assertIsNotNone(user)
        self.assertIsNotNone(profile)
        self.assertEquals(profile.email, user.email)
        self.assertEquals(user.first_name, profile.name)
        self.assertEquals(user.username, profile.username)
        self.assertEquals(user, profile.user)

    def test_update_user_when_profile_is_updated(self):
        user, profile = self.__create_user_and_profile()
        profile.name = 'Test'
        profile.save()
        user = User.objects.first()
        self.assertEquals(user.first_name, profile.name)

    def test_delete_user_when_profile_is_deleted(self):
        user, profile = self.__create_user_and_profile()
        self.assertIsNotNone(profile)
        profile.delete()
        user = User.objects.first()
        self.assertIsNone(user)
