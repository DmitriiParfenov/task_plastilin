from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from converter.models import Converter
from converter.permissions import IsActiveAndIsOwner
from converter.serializers import ConverterSerializer, ConverterDetailSerializer, ConverterUpdateSerializer, \
    ConverterGetCurrencyRate


# Create your views here.
class ConverterCreateAPIView(generics.CreateAPIView):
    """Для создания объектов модели Converter."""

    serializer_class = ConverterSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Метод сохраняет текущий сериализатор и присваивает полю <converter_user> текущего пользователя. Если
        пользователь введет другого пользователя в поле <converter_user>, то возбудится исключение."""

        converter_user_from_user = serializer.validated_data.get('converter_user')
        if converter_user_from_user != self.request.user:
            raise ValidationError({"converter_user": "Вы указали чужого пользователя."})
        new_mat = serializer.save()
        if not self.request.user.is_staff:
            new_mat.converter_user = self.request.user
        new_mat.save()


class ConverterDetailAPIView(generics.RetrieveAPIView):
    """Для получения детальной информации объектов модели Converter."""

    serializer_class = ConverterDetailSerializer
    queryset = Converter.objects.all()
    permission_classes = (IsActiveAndIsOwner,)


class ConverterUpdateAPIView(generics.UpdateAPIView):
    """Для изменения детальной информации объектов модели Converter."""

    serializer_class = ConverterUpdateSerializer
    queryset = Converter.objects.all()
    permission_classes = (IsActiveAndIsOwner,)

    def perform_update(self, serializer):
        """Метод сохраняет текущий сериализатор и присваивает полю <converter_user> текущего пользователя. Если
        пользователь введет другого пользователя в поле <converter_user>, то возбудится исключение."""

        code_from_user = serializer.validated_data.get('code')
        converter_by_user = Converter.objects.filter(code=code_from_user.upper(),
                                                     converter_user=self.request.user).first()
        if not converter_by_user:
            raise ValidationError({"wrong_code": "Вы не добавляли валюту для конвертации."})
        new_mat = serializer.save()
        if not self.request.user.is_staff:
            new_mat.converter_user = self.request.user
        new_mat.save()


class ConverterGetCurrencyRateAPIView(APIView):
    """Для получения конвертации курса валют, полученных от пользователя."""
    permission_classes = (IsActiveAndIsOwner,)

    def post(self, request):
        serializer = ConverterGetCurrencyRate(data=request.data)
        if serializer.is_valid():

            # Получение переменных
            base_currency = request.data.get('base_currency')
            target_currency = request.data.get('target_currency')
            amount = request.data.get('amount')

            # Получение объекта с курсами валют, созданного пользователем
            user_converter = Converter.objects.filter(code=base_currency.upper(), converter_user=request.user).first()

            # Если объекта с курсами валют нет, то вернется сообщение об этом с 400 статус кодом
            if not user_converter:
                return Response({'converter_user': 'Пользователь не добавил текущую валюту для конвертации.'},
                                status=400)

            # Получение объекта с курсами валют из базы данных
            rate_data = user_converter.rate.get(code=target_currency.upper())

            # Если объекта с курсами валют из базы данных нет, то вернется сообщение об этом с 400 статус кодом
            if not rate_data:
                return Response({'converter_user': 'Пользователь не добавил текущую валюту для конвертации.'},
                                status=400)

            # Конвертация валюты
            result = rate_data.currency_rate * int(amount)
            return Response({'converter': f'{amount} {base_currency} = {result} {target_currency}'})
        return Response(serializer.errors, status=400)
