from django.db import models


# Create your models here.
class Converter(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    code = models.CharField(max_length=3, verbose_name='Код')
    rate = models.ManyToManyField('converter.CurrencyRate', verbose_name='курс')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')
    changed = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Дата изменения')
    converter_user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Создатель')

    def __str__(self):
        return f'Конвертер {self.title}.'

    class Meta:
        verbose_name = 'Конвертер валют'
        verbose_name_plural = 'Конвертеры валют'


class CurrencyRate(models.Model):
    code = models.CharField(max_length=3, verbose_name='Код')
    currency_rate = models.DecimalField(max_digits=50, decimal_places=6)
