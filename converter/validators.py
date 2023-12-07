from rest_framework import serializers

from converter.models import Converter


class CodeValidator:
    """Для валидации поля <code>."""

    def __init__(self, code):
        self.code = code

    def __call__(self, value):
        errors = {}
        action_currencies = {
            'GBP': 'Фунты',
            'USD': 'Доллары',
            'EUR': 'Евро',
            'CNY': 'Йены'
        }
        user_code = value.get(self.code)

        if user_code.upper() not in action_currencies:
            errors['wrong_code'] = 'Необходимо использовать только актуальные курсы валют.'

        if errors:
            raise serializers.ValidationError(errors)


class CodeUserValidator:
    """Для валидации полей <code> и <converter_user>. Если текущий пользователь создаст валюту для конвертации, то
    он не сможет создать второй объект с аналогичной валютой - возбудится исключение."""
    def __init__(self, code, user):
        self.code = code
        self.user = user

    def __call__(self, value):
        # Получение переменных
        errors = {}
        code_from_user = value.get(self.code)
        user_from_user = value.get(self.user)
        currency_by_user = Converter.objects.filter(code=code_from_user.upper(), converter_user=user_from_user).first()
        if currency_by_user:
            errors['unique_code'] = 'Вы уже добавляли валюту для конвертации.'
        if errors:
            raise serializers.ValidationError(errors)
