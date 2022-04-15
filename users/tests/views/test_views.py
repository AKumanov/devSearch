from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.test import TestCase

from users.signals import create_profile

from django.urls import reverse
from projects.models import Project
from users.forms import CustomUserCreationForm, CustomStaffUserCreationForm
from users.models import Profile


class TestUserViews(TestCase):
    __PROJECT_TITLE = 'Test title'
    __USER_DATA = {
        'username': 'jdoe',
        'email': 'jdoe@example.com',
        'password': 'Some12Strange213'
    }
    __LOGIN_CREDS = {
        'username': 'jdoe',
        'password': 'Some12Strange213',
    }

    _REGISTER_CREDS = {
        'first_name': 'Alexander',
        'email': 'test_user@abv.bg',
        'username': 'kumana',
        'password1': '901209#Method',
        'password2': '901209#Method'
    }
    __INVALID_REGISTER_CREDS = {
        'first_name': 'Alexander',
        'email': 'test_user@abv.bg',
        'username': 'kumana',
        'password1': '901209#Method',
        'password2': 'diffPass123'
    }

    @staticmethod
    def __create_permission_group():
        group = Group.objects.create(
            name='Staff'
        )
        group.save()
        return group

    def __get_user_and_profile_objects(self):
        user = User(**self.__USER_DATA)
        user.save()
        profile = Profile.objects.get(user=user)
        return user, profile

    def __create_project(self, profile):
        project = Project(
            owner=profile,
            title=self.__PROJECT_TITLE
        )
        project.save()
        return project

    def test_all_profiles_view(self):
        response = self.client.get(reverse('profiles'))
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'users/profiles.html')

    def test_get_user_profile_view(self):
        user, profile = self.__get_user_and_profile_objects()
        self.assertIsNotNone(user)
        self.assertIsNotNone(profile)

        project = self.__create_project(profile)
        self.assertIsNotNone(project)
        self.assertEquals(project.owner, profile)
        response = self.client.get(reverse('user-profile', args=[profile.id]))
        self.assertEquals(200, response.status_code)
        project = Project.objects.get(title='Test title')
        self.assertIsNotNone(project)
        self.assertEquals(profile, project.owner)

        context_profile = response.context['profile']
        context_projects = response.context['projects']
        self.assertEquals(profile, context_profile)
        self.assertTrue('projects' in response.context)
        self.assertEquals(1, len(context_projects))
        self.assertEquals('Test title', context_projects[0].title)

    def test_user_account_view_get_if_user_is_not_logged_in_redirects_to_login_page(self):
        user, profile = self.__get_user_and_profile_objects()
        project = self.__create_project(profile)
        self.assertEquals(project.owner, profile)
        self.assertIsNotNone(project)
        response = self.client.get(reverse('account'))
        code = response.status_code
        self.assertEquals(302, code)
        self.assertTemplateUsed('users/login_register.html')

    def test_registration_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'users/login_register.html')
        self.failUnless(isinstance(response.context['form'], CustomUserCreationForm))

    def test_registration_view_post_success(self):
        response = self.client.post(reverse('register'), self._REGISTER_CREDS)
        self.assertEquals(302, response.status_code)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
        self.assertRedirects(response, reverse('edit-account'))

    def test_registration_view_post_failure(self):
        response = self.client.post(reverse('register'), self.__INVALID_REGISTER_CREDS)
        self.assertEquals(200, response.status_code)
        self.failIf(response.context['form'].is_valid())

    def test_registration_complete_view_get(self):
        response = self.client.post(reverse('register'), self._REGISTER_CREDS)
        self.assertEquals(302, response.status_code)
        profile = Profile.objects.first()
        users = get_user_model()
        user = users.objects.all()[0]
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.is_active)
        self.assertIsNotNone(profile)
        self.assertEquals(profile.name, self._REGISTER_CREDS['first_name'])
        self.assertEquals(profile.email, self._REGISTER_CREDS['email'])
        self.assertEquals(profile.username, self._REGISTER_CREDS['username'])

    def test_registration_staff_view_get(self):
        response = self.client.get(reverse('register-staff'))
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'users/login_register_staff.html')
        self.failUnless(isinstance(response.context['form'], CustomStaffUserCreationForm))

    def test_register_staff_view_post_success(self):
        group = self.__create_permission_group()
        response = self.client.post(reverse('register-staff'), self._REGISTER_CREDS)
        self.assertEquals(302, response.status_code)
        users = get_user_model()
        user = users.objects.all()[0]
        self.assertIsNotNone(user)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.groups.filter(name=group.name).exists())
        self.assertFalse(user.has_perm('blog.delete_post'))
        self.assertRedirects(response, reverse('edit-account'))

    def test_register_view_post_failure(self):
        response = self.client.post(reverse('register-staff'), self.__INVALID_REGISTER_CREDS)
        self.assertEquals(200, response.status_code)
        self.failIf(response.context['form'].is_valid())

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(200, response.status_code)


class TestSkillViews(TestCase):
    __USER_DATA = {
        'username': 'jdoe',
        'email': 'jdoe@example.com',
        'password': 'Some12Strange213'
    }

    def __register_user(self):
        self.client.login(username='kumana', password='901209Method')
        return

    def __get_user_and_profile_objects(self):
        user = User(**self.__USER_DATA)
        user.save()
        profile = Profile.objects.get(user=user)
        self.client.login(username=user.username, password=user.password)
        return user, profile

    # def test_create_skill(self):
    #     user, profile = self.__get_user_and_profile_objects()
    #     self.assertIsNotNone(user)
    #     self.assertTrue(user.is_authenticated)
    #     self.assertTrue(user.is_active)
    #     response = self.client.post(reverse('create-skill'))
    #     # session = self.client.session
    #     code = response.status_code
    #     pass

