from django.test import TestCase

from blog.forms import CreatePostForm
from blog.models import Topic


class PostCreateTest(TestCase):

    def test_post_formCreate_whenValid_data(self):
        topic = Topic(
            title='New Topic'
        )
        topic.save()
        data = {
            'title': 'Test Title',
            'topic': topic,
            'description': 'test description',
            'body': 'Test content'
        }
        form = CreatePostForm(data)
        self.assertTrue(form.is_valid())

    def test_post_formCreate__whenInvalid_topic(self):
        data = {
            'title': 'Test Title',
            'topic': 'Invalid Topic',
            'description': 'test desc',
            'body': 'test body'
        }

        form = CreatePostForm(data)
        self.assertFalse(form.is_valid())