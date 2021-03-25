from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title='Название',
            slug='test-slug',
            description='Описание',
        )
        cls.post = Post.objects.create(
            text='Текст поста',
            group=cls.group,
            author=User.objects.create(username='author post'),
        )

    def setUp(self):
        """Authorized users have access to the page with the model."""

        self.user = User.objects.create_user(username='Tester')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_add_new_post(self):
        """Check that after creating a post,
        the number of posts has changed,
        and check the statute code.
        """

        posts_count = Post.objects.count()
        form_data = {
            # 'title': 'Заголовок из формы',
            'text': 'Тестовый пост для проверки count',
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertNotEqual(Post.objects.count(), posts_count)
        self.assertEqual(response.status_code, 200)
