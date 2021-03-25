from django.test import TestCase

from posts.models import Group, Post, User


class FieldPostGroupModelTest(TestCase):
    """Class Test for K: verbose name, help text field.
    And expected self methods.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Название',
            slug='Слаг',
            description='Описание',
        )
        cls.post = Post.objects.create(
            text='Текст поста',
            group=cls.group,
            author=User.objects.create(username='tester'),
        )

    def test_verbose_name(self):
        post = FieldPostGroupModelTest.post
        field_verbose = {
            'text': 'Тело поста',
            'group': 'Группа',
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected
                )

    def test_help_text(self):
        post = FieldPostGroupModelTest.post
        field_help_text = {
            'text': 'Наполнить пост',
            'group': 'Выбор группы не обязателен, но желателен',
        }
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                )

    def test_object_name_is_title_field(self):
        group = FieldPostGroupModelTest.group
        expected_object_name = group.title
        self.assertEquals(expected_object_name, str(group))

    def test_str_post(self):
        post = FieldPostGroupModelTest.post
        expected_length_string = post.text[:15]
        self.assertEquals(expected_length_string, str(post))
