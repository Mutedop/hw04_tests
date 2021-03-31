from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


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
        cls.group_two = Group.objects.create(
            title='Название 2',
            slug='test-slug-two',
            description='Описание 2',
        )
        cls.post = Post.objects.create(
            id=123,
            text='Текст поста',
            group=cls.group,
            author=cls.author_post,
        )
        posts_items = [Post(
            text=f'Пост № {number_post}',
            author=cls.author_post,
            group=cls.group) for number_post in range(12)]
        Post.objects.bulk_create(posts_items)

    def setUp(self) -> User:
        self.user = User.objects.create_user(username='Tester')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        """Try using reverse for names.
        I check the work args & kwargs for r_name, url's
        """

        template_pages = {
            'new.html': reverse('new_post'),
            'post.html': (reverse('post',
                          kwargs={'username': 'AuthorPost',
                                  'post_id': '123'})),
            'index.html': reverse('index'),
            'group.html': (reverse('group_post',
                           args={'test-slug'})),
            'profile.html': (reverse('profile',
                             args={'Tester'})),
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
        then this post appears on the main page of the site,
        on the page of the selected group.
        Make sure this post is not in a group it was not intended for.
        """

        posts_count_group = Post.objects.filter(
            group=PagesTest.group
        ).count()
        posts_count_group_two = Post.objects.filter(
            group=PagesTest.group_two
        ).count()
        post_count = Post.objects.count()
        
        date_field = {
            'text': 'Создаем пост для сущ. группы',
            'group': PagesTest.group.id
        }
        
        response = self.authorized_client.post(
            reverse('new_post'),
            data=date_field,
            follow=True
        )
        
        # Checked the appearance of the created post.
        self.assertNotEqual(Post.objects.count(), post_count)
        # I checked that after the creation they went to the main page.
        self.assertRedirects(response, reverse('index'))
        # I checked the create text field that the post is in the group 1.
        self.assertTrue(Post.objects.filter(
            text='Создаем пост для сущ. группы',
            group=PagesTest.group.id
        ).exists())
        # Compare the number of posts in group one.
        self.assertNotEqual(Post.objects.filter(
            group=PagesTest.group).count(), posts_count_group
        )
        # I checked the text field that the post is in the group_two 2.
        self.assertFalse(Post.objects.filter(
            text='Создаем пост для сущ. группы',
            group=PagesTest.group_two.id
        ).exists())
        # Compare the number of posts in group 2.
        self.assertEqual(Post.objects.filter(
            group=PagesTest.group_two).count(), posts_count_group_two
        )

    def test_post_edit_correct_context(self):
        response = PagesTest.author_client.get(
            reverse('post_edit',
                    kwargs={
                        'username': 'AuthorPost',
                        'post_id': '123'
                    })
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_profile_correct_context(self):
        response = self.authorized_client.get(
            reverse('profile', args={'AuthorPost'})
        )
        post_object = response.context['page'][0]
        post_author_0 = post_object.author
        post_text_0 = post_object.text
        self.assertEqual(post_author_0,
                         PagesTest.post.author)
        self.assertEqual(post_text_0,
                         PagesTest.post.text)
