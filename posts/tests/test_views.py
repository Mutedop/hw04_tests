from posts.forms import PostForm
from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author_post = User.objects.create_user(username='AuthorPost')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author_post)
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Название',
            slug='test-slug',
            description='Описание',
        )
        cls.post = Post.objects.create(
            id=1,
            text='Текст поста',
            group=cls.group,
            author=cls.author_post,
        )
        for post in range(12):
            Post.objects.create(
                text=f'Текст поста {post}',
                author=cls.author_post,
                group=cls.group,
            )
        cls.form = PostForm()

    def setUp(self) -> User:
        self.user = User.objects.create_user(username='Tester')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        """Try using reverse for names."""
        template_pages = {
            'new.html': reverse('new_post'),
            'index.html': reverse('index'),
            'group.html': reverse(
                'group_post',
                kwargs={'slug': 'test-slug'}),
        }
        for template, reverse_name in template_pages.items():
            with self.subTest(template=template):
                response = (self.authorized_client.
                            get(reverse_name))
                self.assertTemplateUsed(response, template)

    def test_index_correct_context(self):
        response = self.authorized_client.get(reverse('index'))
        post_object = response.context['page'][0]
        post_author_0 = post_object.author
        post_pub_date_0 = post_object.pub_date
        post_text_0 = post_object.text
        self.assertEqual(post_author_0,
                         PagesTest.post.author)
        self.assertEqual(post_pub_date_0,
                         PagesTest.post.pub_date)
        self.assertEqual(post_text_0,
                         PagesTest.post.text)

    def test_group_correct_context(self):
        response = self.authorized_client.get(
            reverse('group_post',
                    kwargs={'slug': 'test-slug'}))
        self.assertEqual(
            response.context['group'].title,
            'Название')
        self.assertEqual(
            response.context['group'].description,
            'Описание')
        self.assertEqual(
            response.context['group'].slug,
            'test-slug')

    def test_new_post_correct_context(self):
        response = (self.authorized_client.
                    get(reverse('new_post')))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_index_page_paginator(self):
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_create_post_on_view(self):
        """Check that if you specify a group when creating a post,
        then this post appears. On the home page of the site.
        """

        post_count = Post.objects.count()
        date_field = {
            'text': 'Создаем пост для сущ. группы',
            'group': PagesTest.group.id
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            date=date_field,
            follow=True
        )
        self.assertNotEqual(Post.objects.count(), post_count)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(Post.objects.filter(
            text='Создаем пост для сущ. группы',
            group=PagesTest.group.id
        ).exists())
