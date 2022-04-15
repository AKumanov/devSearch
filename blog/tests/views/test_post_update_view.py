from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post
from users.models import Profile


class UpdatePostTest(TestCase):
    def test_update_post_with_valid_information(self):
        user = User.objects.create(
            first_name='Alexander',
            email='kumana@abv.bg',
            password='901209#Method'
        )
        user.save()

        profile = Profile.objects.get()

        post = Post.objects.create(
            owner=profile,
            title='Test post'
        )
        post.save()
        post_data = {
            'title': 'Test post - Upd'
        }
        self.client.post(
            reverse('post-update', kwargs={
                post.id
            }),
            data=post_data

        )
        post.save()
        post = Post.objects.first()
        self.assertEqual('Test Post - Upd', post.title)
