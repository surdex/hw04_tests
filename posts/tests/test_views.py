from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='test_user',
            first_name='Name',
            last_name='Surname'
        )
        cls.group_with_post = Group.objects.create(
            title='Test Group with post',
            slug='test-slug-of-group-with-post',
            description='Test group(1) description',
        )
        cls.group_without_post = Group.objects.create(
            title='Test Group without post',
            slug='test-slug-of-group-without-post',
            description='Test group(2) description',
        )
        cls.post = Post.objects.create(
            text='Test text',
            author=cls.user,
            group=cls.group_with_post,
        )
        kwarg_for_post = {
            'username': PostPagesTests.user.username,
            'post_id': PostPagesTests.post.id
        }
        cls.templates_page_names = {
            'index.html': reverse('index'),
            'group.html': reverse(
                'group',
                kwargs={'slug': PostPagesTests.group_with_post.slug}
            ),
            'new_post.html': {
                'new_post': reverse('new_post'),
                'edit_post': reverse('post_edit', kwargs=kwarg_for_post)
            },
            'post.html': reverse('post', kwargs=kwarg_for_post),
            'profile.html': reverse(
                'profile',
                kwargs={'username': PostPagesTests.user.username}
            )
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)

    def test_pages_post_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = PostPagesTests.templates_page_names
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                if template != 'new_post.html':
                    response = self.authorized_client.get(reverse_name)
                    self.assertTemplateUsed(response, template)

    def test_pages_post_correct_template_new_post(self):
        """URL-адреса использует шаблон new_post.html."""
        pages_name = PostPagesTests.templates_page_names['new_post.html']
        for reverse_name in pages_name.values():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, 'new_post.html')

    def test_index_pages_show_correct_context(self):
        """Шаблон index сформированы с правильным контекстом."""
        response = self.guest_client.get(reverse('index'))
        self.assertIn('page', response.context)
        first_object = response.context['page'][0]
        self.assertEqual(first_object.text, PostPagesTests.post.text)
        self.assertEqual(first_object.pub_date, PostPagesTests.post.pub_date)
        self.assertEqual(first_object.author, PostPagesTests.post.author)

    def test_group_with_post_pages_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            self.templates_page_names['group.html']
        )
        self.assertIn('page', response.context)
        self.assertIn('group', response.context)
        first_object = response.context['page'][0]
        self.assertEqual(first_object.text, PostPagesTests.post.text)
        self.assertEqual(first_object.pub_date, PostPagesTests.post.pub_date)
        self.assertEqual(first_object.author, PostPagesTests.post.author)
        response_group = response.context['group']
        group = PostPagesTests.group_with_post
        self.assertEqual(response_group.title, group.title)
        self.assertEqual(response_group.slug, group.slug)
        self.assertEqual(response_group.description, group.description)

    def test_group_page_without_post_has_correct_context(self):
        """Созданные посты относятся только к выбранной группе."""
        response = self.authorized_client.get(
            reverse(
                'group',
                kwargs={'slug': PostPagesTests.group_without_post.slug}
            )
        )
        self.assertNotIn(PostPagesTests.post, response.context['page'])

    def test_new_post_page_show_correct_context(self):
        """Шаблон new post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        self.assertIn('form', response.context)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        templates_page_names = PostPagesTests.templates_page_names
        response = self.authorized_client.get(
            templates_page_names['profile.html']
        )
        self.assertIn('page', response.context)
        self.assertIn('author', response.context)
        self.assertIn('count_posts', response.context)
        page_object = response.context['page'][0]
        self.assertEqual(page_object.text, PostPagesTests.post.text)
        self.assertEqual(page_object.pub_date, PostPagesTests.post.pub_date)
        self.assertEqual(page_object.author, PostPagesTests.post.author)
        self.assertEqual(page_object.id, PostPagesTests.post.id)
        author_object = response.context['author']
        self.assertEqual(author_object.get_full_name(),
                         PostPagesTests.user.get_full_name())
        self.assertEqual(author_object.get_username(),
                         PostPagesTests.user.username)
        count_posts = response.context['count_posts']
        self.assertEqual(count_posts, PostPagesTests.user.posts.count())

    def test_post_page_show_correct_context(self):
        """Шаблон post сформирован с правильным контекстом."""
        templates_page_names = PostPagesTests.templates_page_names
        response = self.authorized_client.get(
            templates_page_names['post.html']
        )
        self.assertIn('post', response.context)
        self.assertIn('author', response.context)
        self.assertIn('count_posts', response.context)
        page_object = response.context['post']
        self.assertEqual(page_object.text, PostPagesTests.post.text)
        self.assertEqual(page_object.pub_date, PostPagesTests.post.pub_date)
        self.assertEqual(page_object.author, PostPagesTests.post.author)
        self.assertEqual(page_object.id, PostPagesTests.post.id)
        author_object = response.context['author']
        self.assertEqual(author_object.get_full_name(),
                         PostPagesTests.user.get_full_name())
        self.assertEqual(author_object.get_username(),
                         PostPagesTests.user.username)
        count_posts = response.context['count_posts']
        self.assertEqual(count_posts, PostPagesTests.user.posts.count())

    def test_paginator_show_correct_context(self):
        """Проверка правильности контекста paginator на всех страницах"""
        for ten_posts in range(10):
            Post.objects.create(
                text='Infinity text',
                author=PostPagesTests.user,
                group=PostPagesTests.group_with_post
            )
        templates_page_names = PostPagesTests.templates_page_names
        pages_with_paginator = ['index.html', 'group.html', 'profile.html']
        for page_names in pages_with_paginator:
            with self.subTest(page_names=page_names):
                response = self.guest_client.get(
                    templates_page_names[page_names]
                )
                count_objects = len(response.context['page'])
                self.assertEqual(count_objects, 10)

    def test_post_edit_page_show_correct_context(self):
        """Отредактированные посты сохранены в БД."""
        template_page = PostPagesTests.templates_page_names['new_post.html']
        response = self.authorized_client.get(template_page['edit_post'])
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
        page_object = response.context['post']
        self.assertEqual(page_object.text, PostPagesTests.post.text)
        self.assertEqual(page_object.group, PostPagesTests.post.group)
