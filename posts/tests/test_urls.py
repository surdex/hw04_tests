from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.user_without_posts = User.objects.create_user(
            username='user_without_posts'
        )
        cls.group = Group.objects.create(
            title='Test Group',
            slug='test-slug-of-group',
            description='Test group description',
        )
        cls.post = Post.objects.create(
            text='Test text',
            author=cls.user,
            group=cls.group,
        )
        cls.URLs_list_for_guest = [
            reverse('index'),
            '/group/test-slug-of-group/',
            '/test_user/',
            f'/test_user/{cls.post.id}/',
        ]
        cls.URLs_list_for_authorized = [
            '/new/',
            f'/test_user/{cls.post.id}/edit/',
        ]

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(StaticURLTests.user)
        self.authorized_client_without_posts = Client()
        self.authorized_client_without_posts.force_login(
            StaticURLTests.user_without_posts
        )

    def test_URls_exists_at_desired_location_for_guest(self):
        """Страницы доступные любому пользователю."""
        for url in StaticURLTests.URLs_list_for_guest:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_URls_exists_at_desired_location_only_for_authorized(self):
        """Страницы доступные только авторизованному автору поста."""
        for url in StaticURLTests.URLs_list_for_authorized:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_new_and_post_edit_url_redirect_anonymous(self):
        """Страницы перенаправляющие анониного пользователя."""
        for url in StaticURLTests.URLs_list_for_authorized:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, '/auth/login/?next=' + url)

    def test_post_edit_url_redirect_authorized_on_post_page(self):
        """Страница post_edit перенаправляет не автора поста."""
        post_id = StaticURLTests.post.id
        response = self.authorized_client_without_posts.get(
            f'/test_user/{post_id}/edit/',
            follow=True
        )
        self.assertRedirects(response, f'/test_user/{post_id}/')

    # Этот модуль дублируется в test_views.
    # Где он должен правильно находиться, тут или в test_views?
    # def test_urls_uses_correct_template(self):
    #    templates_url_names = {
    #        'index.html': '/',
    #        'group.html': reverse(
    #            'group',
    #            kwargs={'slug': 'test-slug-of-group'}
    #        ),
    #        'new_post.html': '/new/',
    #    }
    #    for template, url in templates_url_names.items():
    #        with self.subTest(url=url):
    #            response = self.authorized_client.get(url)
    #            self.assertTemplateUsed(response, template)
