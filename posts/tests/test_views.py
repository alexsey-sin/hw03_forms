from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group
from django import forms

User = get_user_model()


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса group/note/
        Group.objects.create(
            title='Заметки',
            slug='note',
            description='Небольшие заметки любого содержания',
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='template_user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: name"
        templates_pages_names = {
            'index.html': reverse('index'),
            'group.html': reverse('group', kwargs={'slug': 'note'}),
            'new_post.html': reverse('new_post'),
        }
        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверка словаря контекста главной страницы (в нём передаётся форма)
    def test_home_page_shows_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            # При создании формы поля модели типа TextField
            # преобразуются в CharField с виджетом forms.Textarea
            'text': forms.fields.CharField,
            'pub_date': forms.fields.DateTimeField,
            'author': forms.fields.CharField,
            'group': forms.fields.CharField,
        }

        # Проверяем, что типы полей формы в словаре context соответствуют ожиданиям
        # for value, expected in form_fields.items():
        #     with self.subTest(value=value):
        #         form_field = response.context['form'].fields[value]
        #         # Проверяет, что поле формы является экземпляром указанного класса
        #         self.assertIsInstance(form_field, expected)

    # # Проверяем, что словарь context страницы со списком задач
    # # в первом элементе списка object_list содержит ожидаемые значения
    # def test_task_list_page_shows_correct_context(self):
    #     """Шаблон task_list сформирован с правильным контекстом."""
    #     response = self.authorized_client.get(reverse('deals:task_list'))
    #     # Взяли первый элемент из списка и проверили, что его содержание
    #     # совпадает с ожидаемым
    #     first_object = response.context['object_list'][0]
    #     task_title_0 = first_object.title
    #     task_text_0 = first_object.text
    #     task_slug_0 = first_object.slug
    #     self.assertEqual(task_title_0, 'Заголовок')
    #     self.assertEqual(task_text_0, 'Текст')
    #     self.assertEqual(task_slug_0, 'test-slug')
    #
    # # Проверяем, что словарь context страницы task/test-slug
    # # содержит ожидаемые значения
    # def test_task_detail_pages_show_correct_context(self):
    #     """Шаблон task_detail сформирован с правильным контекстом."""
    #     response = self.authorized_client.get(
    #             reverse('deals:task_detail', kwargs={'slug': 'test-slug'})
    #     )
    #     self.assertEqual(response.context['task'].title, 'Заголовок')
    #     self.assertEqual(response.context['task'].text, 'Текст')
    #     self.assertEqual(response.context['task'].slug, 'test-slug')
