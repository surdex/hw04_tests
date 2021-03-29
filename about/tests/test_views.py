from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.reverse_pages = {
            'about/tech.html': reverse('about:tech'),
            'about/author.html': reverse('about:author')
        }

    def test_about_page_accessible_by_name(self):
        """URL, генерируемый при помощи имени static_pages:about, доступен."""
        for reverse_page in self.reverse_pages.values():
            with self.subTest(reverse_page=reverse_page):
                response = self.guest_client.get(reverse_page)
                self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        """При запросе к staticpages:about
        применяется шаблон staticpages/about.html."""
        for template, reverse_page in self.reverse_pages.items():
            with self.subTest(reverse_page=reverse_page):
                response = self.guest_client.get(reverse_page)
                self.assertTemplateUsed(response, template)
