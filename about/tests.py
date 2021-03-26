from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.template_pages = {
            'about/tech.html': reverse('about:tech'),
            'about/author.html': reverse('about:author'),
        }

    def test_static_page_uses_correct_template(self):
        for template, reverse_name in self.template_pages.items():
            with self.subTest(template=template):
                response = (self.guest_client.
                            get(reverse_name))
                self.assertTemplateUsed(response, template)

    def test_static_page_status_code(self):
        for template, reverse_name in self.template_pages.items():
            with self.subTest(template=template):
                response = (self.guest_client.
                            get(reverse_name))
                self.assertEqual(response.status_code, 200)
