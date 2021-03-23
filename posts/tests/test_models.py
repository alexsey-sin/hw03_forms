from django.db.transaction import TransactionManagementError
from django.test import TestCase
from posts.models import Group, Post


class GroupModelTest(TestCase):
    task = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        cls.task = Group.objects.create(
            title='ж'*200,
            description='Тестовый текст',
        )

    def test_object_name_is_title_field(self):
        """__str__  task - это строчка с содержимым task.title."""
        task = GroupModelTest.task
        expected_object_name = task.title
        self.assertEquals(expected_object_name, str(task))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = GroupModelTest.task
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Адрес',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        task = GroupModelTest.task
        field_help_texts = {
            'title': 'Дайте короткое название группе',
            'slug': 'Укажите адрес для страницы группы',
            'description': 'Укажите краткое описание группы',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_fild(self):
        """В поле __str__  объекта task записано значение поля task.title."""
        task = GroupModelTest.task
        expected_object_name = task.title
        self.assertEqual(expected_object_name, str(task))


class PostModelTest(TestCase):
    task = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        cls.task = Post.objects.create(
            text='Тестовый текст',
        )

    def test_object_name_is_title_field(self):
        """__str__  task - это строчка с содержимым task.title."""
        with self.assertRaises(TransactionManagementError):
            task = PostModelTest.task
            # expected_object_name = task.text
            pass
        #     do_something()
        # self.assertEquals(expected_object_name, str(task))

    # def test_verbose_name(self):
    #     """verbose_name в полях совпадает с ожидаемым."""
    #     task = GroupModelTest.task
    #     field_verboses = {
    #         'title': 'Заголовок',
    #         'slug': 'Адрес',
    #         'description': 'Описание',
    #     }
    #     for value, expected in field_verboses.items():
    #         with self.subTest(value=value):
    #             self.assertEqual(
    #                 task._meta.get_field(value).verbose_name, expected)
    #
    # def test_help_text(self):
    #     """help_text в полях совпадает с ожидаемым."""
    #     task = GroupModelTest.task
    #     field_help_texts = {
    #         'title': 'Дайте короткое название группе',
    #         'slug': 'Укажите адрес для страницы группы',
    #         'description': 'Укажите краткое описание группы',
    #     }
    #     for value, expected in field_help_texts.items():
    #         with self.subTest(value=value):
    #             self.assertEqual(
    #                 task._meta.get_field(value).help_text, expected)
    #
    # def test_object_name_is_title_fild(self):
    #     """В поле __str__  объекта task записано значение поля task.title."""
    #     task = GroupModelTest.task
    #     expected_object_name = task.title
    #     self.assertEqual(expected_object_name, str(task))
