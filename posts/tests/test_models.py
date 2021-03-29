from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='тест' * 20,
            author=User.objects.create_user(username='test_user'),
        )

    def test_str_method(self):
        post = PostModelTest.post
        expected_object = post.text[:15]
        self.assertEqual(expected_object, str(post))


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test group',
            slug='test-group',
        )

    def test_str_method(self):
        group = GroupModelTest.group
        expected_object = group.title
        self.assertEqual(expected_object, str(group))
