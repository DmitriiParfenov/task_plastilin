from django.urls import path

from converter.apps import ConverterConfig
from converter.views import ConverterCreateAPIView, ConverterDetailAPIView, ConverterUpdateAPIView, \
    ConverterGetCurrencyRateAPIView

app_name = ConverterConfig.name

urlpatterns = [
    path('create/', ConverterCreateAPIView.as_view(), name='create_converter'),
    path('<int:pk>/', ConverterDetailAPIView.as_view(), name='detail_converter'),
    path('update/<int:pk>/', ConverterUpdateAPIView.as_view(), name='update_converter'),
    path('get_rate/', ConverterGetCurrencyRateAPIView.as_view(), name='get_rate_converter')
]
