from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class ModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='тест' * 20,
            author=User.objects.create_user(username='test_user'),
        )
        cls.group = Group.objects.create(
            title='test group',
            slug='test-group',
        )

    def test_str_method(self):
        post = ModelTest.post
        group = ModelTest.group
        expected_objects = [(post.text[:15], str(post)),
                            (group.title, str(group))]
        for expected in expected_objects:
            with self.subTest(expected=expected[0]):
                self.assertEqual(expected[0], expected[1])
