from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class FoodgramUserTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    def test_models_have_correct_object_names(self):
        useername = 'auth'
        self.assertEqual(useername, str(FoodgramUserTest.user))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        user = FoodgramUserTest.user
        field_verboses = {
            'username': 'Логин пользователя, username',
            'email': 'Адрес email',
            'first_name': 'Имя пользователя',
            'last_name': 'Фамилия пользователя',
            'password': 'Пароль',
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    user._meta.get_field(field).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        user = FoodgramUserTest.user
        field_help = {
            'username': 'Введите свой логин',
            'email': 'Введите адрес email',
            'first_name': 'Введите своё имя',
            'last_name': 'Введите фамилию',
            'password': 'Введите пароль',
        }
        for field, expected in field_help.items():
            with self.subTest(field=field):
                self.assertEqual(
                    user._meta.get_field(field).help_text, expected)
