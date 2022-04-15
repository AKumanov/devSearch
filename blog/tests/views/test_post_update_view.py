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
        post_data = {
            'title': 'Test post - Upd'
        }
        response = self.client.post(reverse('post-update', args=[post.id]), data=post_data)
        self.assertEqual(302, response.status_code)
        post = Post.objects.first()
        self.assertEqual(post_data['title'], post.title)

