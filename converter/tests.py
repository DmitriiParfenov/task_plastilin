from rest_framework import status

from converter.models import Converter, CurrencyRate
from users.tests import UserModelTestCase


# Create your tests here.
class ConverterModelTestCase(UserModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Создание объектов Converter
        self.converter_1 = Converter.objects.create(
            title='Доллар',
            code='USD',
            converter_user=self.user_test
        )
        self.converter_1.save()

        self.converter_2 = Converter.objects.create(
            title='Евро',
            code='EUR',
            converter_user=self.user_2
        )
        self.converter_2.save()

    def tearDown(self) -> None:
        return super().tearDown()


class ConverterCreateTestCase(ConverterModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.sale_create_url = '/converter/create/'

        # Данные для создания объекта Converter
        self.converter_create_data = {
            'title': 'Фунты',
            'code': 'GBP',
            'converter_user': 'test@test.com',
        }

    def test_user_can_create_converter_correctly(self):
        """Авторизованные пользователи могут создавать объекты модели Converter корректно."""

        # Количество объектов до создания
        self.assertTrue(
            Converter.objects.count() == 2
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.converter_create_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Количество объектов после создания
        self.assertTrue(
            Converter.objects.count() == 3
        )

        # Количество валют для конвертации после создания
        self.assertTrue(
            CurrencyRate.objects.count() == 3
        )

    def test_user_cannot_create_converter_without_authentication(self):
        """Неавторизованные пользователи не могут создавать объекты Converter."""

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.converter_create_data,
            headers=None,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_create_converter_without_actual_currencies(self):
        """Авторизованные пользователи не могут создавать объекты модели Converter с неактуальными валютами."""

        # Количество объектов до создания
        self.assertTrue(
            Converter.objects.count() == 2
        )

        # Данные для создания объекта Converter
        self.converter_create_data_1 = {
            'title': 'Драмы',
            'code': 'AMD',
            'converter_user': 'test@test.com',
        }

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.converter_create_data_1,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Converter.objects.count() == 2
        )

        # Количество валют для конвертации после создания
        self.assertTrue(
            CurrencyRate.objects.count() == 0
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'wrong_code': ['Необходимо использовать только актуальные курсы валют.']}
        )

    def test_user_cannot_create_converter_with_wrong_converter_user(self):
        """Авторизованные пользователи не могут создавать объекты модели Converter, указывая чужого пользователя."""

        # Количество объектов до создания
        self.assertTrue(
            Converter.objects.count() == 2
        )

        # Данные для создания объекта Converter
        self.converter_create_data_1 = {
            'title': 'Доллар',
            'code': 'USD',
            'converter_user': 'another@test.com',
        }

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.converter_create_data_1,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Converter.objects.count() == 2
        )

        # Количество валют для конвертации после создания
        self.assertTrue(
            CurrencyRate.objects.count() == 0
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'converter_user': 'Вы указали чужого пользователя.'}
        )

    def test_user_cannot_create_two_unique_converter_objects(self):
        """Авторизованные пользователи не могут создавать объекты модели Converter для одной и той же валюты."""

        # Количество объектов до создания
        self.assertTrue(
            Converter.objects.count() == 2
        )

        # Данные для создания объекта Converter
        self.converter_create_data_1 = {
            'title': 'Доллар',
            'code': 'USD',
            'converter_user': 'test@test.com',
        }

        # Создание объекта Converter
        self.converter_1_copy = Converter.objects.create(
            title='Доллар',
            code='USD',
            converter_user=self.user_test,
        )
        self.converter_1_copy.save()

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.converter_create_data_1,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Converter.objects.count() == 3
        )

        # Количество валют для конвертации после создания
        self.assertTrue(
            CurrencyRate.objects.count() == 0
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'unique_code': ['Вы уже добавляли валюту для конвертации.']}
        )


class ConverterGetDetailTestCase(ConverterModelTestCase):

    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.converter_detail_url = f'/converter/{self.converter_1.pk}/'

    def test_user_can_get_detail_converter_correctly(self):
        """Активные пользователи могут получить информацию об объекте модели Converter корректно."""

        # GET-запрос на получение информации об объекте
        response = self.client.get(
            self.converter_detail_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на создателя объекта
        self.assertEqual(
            response.json().get('converter_user'),
            'test@test.com'
        )

    def test_user_cannot_get_detail_converter_without_authentication(self):
        """Неавторизованные пользователи не могут получить информацию об объекте Converter."""

        # GET-запрос на получение информации об объекте
        response = self.client.get(
            self.converter_detail_url,
            headers=None,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_get_detail_converter_another_user(self):
        """Пользователи не могут получить информацию об объекте Converter чужих пользователей."""

        # GET-запрос на получение информации об объекте
        response = self.client.get(
            self.converter_detail_url,
            headers=self.headers_user_2,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )


class ConverterUpdateTestCase(ConverterModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Запрос на создание тестового объекта
        self.converter_test = self.client.post(
            '/converter/create/',
            {
                'title': 'Йены',
                'code': 'CNY',
                'converter_user': 'test@test.com'
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Получение маршрутов
        self.converter_test_object = Converter.objects.filter(code="CNY", converter_user=self.user_test.pk).first()
        self.converter_update_url = f'/converter/update/{self.converter_test_object.pk}/'

        # Данные для обновления объекта Converter
        self.converter_update_data = {
            'code': 'CNY',
        }

    def test_user_can_update_converter_correctly(self):
        """Авторизованные пользователи могут изменять объекты модели Converter корректно. """

        data_before = self.converter_test_object.changed

        # PATCH-запрос на изменение объекта
        response = self.client.patch(
            self.converter_update_url,
            self.converter_update_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # GET-запрос на получение объекта
        response_1 = self.client.get(
            f'/converter/{self.converter_test_object.pk}/',
            headers=self.headers_user_1,
            format='json'
        )

        # Сравнение дат изменения
        self.assertNotEqual(
            data_before,
            response_1.json().get('changed')
        )

    def test_user_cannot_update_converter_without_authentication(self):
        """Неавторизованные пользователи не могут обновлять объекты Converter."""

        # PATCH-запрос на изменение объекта
        response = self.client.patch(
            self.converter_update_url,
            self.converter_update_data,
            headers=None,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_update_currency_rate_not_actual_currency(self):
        """Авторизованные пользователи не могут обновлять курсы валют, которые не актуальны."""

        # PATCH-запрос на изменение объекта
        response = self.client.patch(
            self.converter_update_url,
            {'code': 'AMD'},
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'wrong_code': ['Необходимо использовать только актуальные курсы валют.']}
        )

    def test_user_cannot_update_currency_rate_before_adding(self):
        """Авторизованные пользователи не могут обновлять курсы валют, которые не добавили."""

        # PATCH-запрос на изменение объекта
        response = self.client.patch(
            self.converter_update_url,
            {'code': 'EUR'},
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'wrong_code': 'Вы не добавляли валюту для конвертации.'}
        )

    def test_user_cannot_update_sales_another_user(self):
        """Авторизованные пользователи не могут изменять детальную информацию объектов модели Converter чужих
        пользователей."""

        # PATCH-запрос на обновление объекта модели тестового пользователя вторым пользователем
        response = self.client.patch(
            self.converter_update_url,
            self.converter_update_data,
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )


class ConverterGetCurrencyRateTestCase(ConverterModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Добавление маршрутов
        self.get_currency_rate = '/converter/get_rate/'

        # Запрос на создание тестового объекта
        self.converter_test = self.client.post(
            '/converter/create/',
            {
                'title': 'Йены',
                'code': 'CNY',
                'converter_user': 'test@test.com'
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Получение маршрутов
        self.converter_test_object = Converter.objects.filter(code="CNY", converter_user=self.user_test.pk).first()

    def test_user_can_get_currency_rate_correctly(self):
        """Авторизованные пользователи делают конвертацию валют корректно."""

        # Данные для конвертации
        self.currencies = {
            'base_currency': 'CNY',
            'target_currency': 'USD',
            'amount': '200',
        }

        # POST-запрос на конвертацию валют
        response = self.client.post(
            self.get_currency_rate,
            self.currencies,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка содержимого ответа
        self.assertTrue(
            response.json().get('converter')
        )

    def test_user_cannot_get_currency_rate_without_authentication(self):
        """Авторизованные пользователи делают конвертацию валют корректно."""

        # Данные для конвертации
        self.currencies = {
            'base_currency': 'CNY',
            'target_currency': 'USD',
            'amount': '200',
        }

        # POST-запрос на конвертацию валют
        response = self.client.post(
            self.get_currency_rate,
            self.currencies,
            headers=None,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_get_currency_rate_not_actual_currency_1(self):
        """Авторизованные пользователи не могут конвертировать курсы валют, которые не актуальны."""

        # POST-запрос на изменение объекта
        response = self.client.post(
            self.get_currency_rate,
            {
                'base_currency': 'AMB',
                'target_currency': 'USD',
                'amount': '200',
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'wrong_code': ['Необходимо использовать только актуальные курсы валют.']}
        )

    def test_user_cannot_get_currency_rate_not_actual_currency_2(self):
        """Авторизованные пользователи не могут конвертировать курсы валют, которые не актуальны."""

        # POST-запрос на изменение объекта
        response = self.client.post(
            self.get_currency_rate,
            {
                'base_currency': 'CNY',
                'target_currency': 'AMB',
                'amount': '200',
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'wrong_code': ['Необходимо использовать только актуальные курсы валют.']}
        )

    def test_user_cannot_get_currency_rate_before_adding(self):
        """Авторизованные пользователи не могут конвертировать курсы валют, которые не добавили."""

        # POST-запрос на изменение объекта
        response = self.client.post(
            self.get_currency_rate,
            {
                'base_currency': 'GBP',
                'target_currency': 'CNY',
                'amount': '200',
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'converter_user': 'Пользователь не добавил текущую валюту для конвертации.'}
        )
