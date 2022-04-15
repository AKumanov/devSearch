from django.test import TestCase
from django.urls import reverse

from blog.models import Topic


class AllPostsListViewTests(TestCase):
    def test_get__expect_status_code_200(self):
        response = self.client.get(reverse("blog-home"))
        self.assertEqual(200, response.status_code)

    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('blog-home'))
        self.assertTemplateUsed(response, template_name='blog/blog_home.html')

    def test_get__expect_context_to_contain_2_topics(self):
        topics_to_create = (
            Topic(title='Test title', description='Test Desc', image='images/air.PNG'),
            Topic(title='Test title2', description='Test Desc2', image='images/air.PNG'),
        )
        Topic.objects.bulk_create(topics_to_create)
        response = self.client.get(reverse('blog-home'))

        topics = response.context['topics']
        title = topics[0].title
        title2 = topics[1].title
        self.assertEqual(2, len(topics))

        self.assertEqual('Test title', title)
        self.assertEqual('Test title2', title2)
