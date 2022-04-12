from django.test import TestCase

from blog.models import Topic


class TopicTests(TestCase):
    VALID_DATA = {
        "title": "Test Topic",
        "description": "Test description"
    }

    def test_topic_create__when_title_below_max_char_expect_success(self):
        topic = Topic(**self.VALID_DATA)
        topic.save()

    def test_topic_str_method__when_valid__expect_correct_str(self):
        topic = Topic(**self.VALID_DATA)

        self.assertEqual("Test Topic", str(topic))

    def test_topic_is_created__when_no_description_is_given(self):
        title = "Test Title"
        topic = Topic(
            title=title
        )
        self.assertIsNotNone(topic)
