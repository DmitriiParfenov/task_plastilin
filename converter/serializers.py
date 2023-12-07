from datetime import datetime

from rest_framework import serializers

from converter.models import Converter, CurrencyRate
from converter.services import get_currency_rate
from converter.validators import CodeValidator, CodeUserValidator
from users.models import User


class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = ('code', 'currency_rate',)


class ConverterSerializer(serializers.ModelSerializer):
    """Для создания объектов модели Converter."""

    converter_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Converter
        fields = ('id', 'title', 'code', 'converter_user')
        validators = [CodeValidator(code='code'),
                      CodeUserValidator(code='code', user='converter_user')]

    def create(self, validated_data):
        """Метод создает объекты модели Converter и в поле <rate> записывает текущие курсы актуальных валют."""

        # Получение переменных
        errors = {}
        code = validated_data.get('code')
        title = validated_data.get('title')
        converter_user = validated_data.get('converter_user')
        converter = Converter.objects.create(title=title, code=code.upper(), converter_user=converter_user)

        # Получение текущих курсов актуальных валют
        rates_data = get_currency_rate(code)

        # Если функция на получение текущих курсов валют возвращает None, то возбуждается исключение
        if not rates_data:
            errors['server_api'] = 'Сервер для получение курса валют недоступен.'
        if errors:
            raise serializers.ValidationError(errors)

        # Для созданной валюты создаются объекты модели CurrencyRate, связанные с текущим объектов через
        # <многие-ко-многим>.
        for data in rates_data:
            rate_object = CurrencyRate.objects.create(code=data, currency_rate=rates_data.get(data))
            converter.rate.add(rate_object)

        return converter


class ConverterDetailSerializer(serializers.ModelSerializer):
    """Для получения детальной информации о текущем объекте модели Converter."""

    rate = CurrencyRateSerializer(many=True)
    converter_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Converter
        fields = ('id', 'title', 'code', 'rate', 'converter_user', 'created', 'changed')


class ConverterUpdateSerializer(serializers.ModelSerializer):
    """Для обновления объектов модели Converter."""

    class Meta:
        model = Converter
        fields = ('code', )
        validators = [CodeValidator(code='code')]

    def update(self, instance, validated_data):
        """Метод обновляет объекты модели Converter и в поле <rate> записывает текущие курсы актуальных валют. Также
        осуществляется изменение поля <changed> на текущие время и дата."""

        # Получение переменных
        errors = {}
        instance.code = instance.code

        # Получение текущих курсов актуальных валют
        rates_data = get_currency_rate(instance.code)

        # Если функция на получение текущих курсов валют возвращает None, то возбуждается исключение
        if not rates_data:
            errors['server_api'] = 'Сервер для получение курса валют недоступен.'
        if errors:
            raise serializers.ValidationError(errors)

        currency_rate = []

        # Обновление объектов модели CurrencyRate, связанных с текущим объектов через <многие-ко-многим>.
        for data in instance.rate.all():
            data.currency_rate = rates_data.get(data.code)
            data.save(update_fields=['currency_rate'])
            currency_rate.append(data)
        instance.rate.set(currency_rate)

        # Изменение поля <changed> текущего объекта
        instance.changed = datetime.now()
        instance.save(update_fields=['changed'])

        return instance


class ConverterGetCurrencyRate(serializers.Serializer):
    """Для конвертации валют по данным из базы данных."""

    base_currency = serializers.CharField(max_length=3)
    target_currency = serializers.CharField(max_length=3)
    amount = serializers.IntegerField()

    class Meta:
        validators = [CodeValidator(code='base_currency'), CodeValidator(code='target_currency')]
