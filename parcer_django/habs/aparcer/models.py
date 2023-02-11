from django.db import models

class Product(models.Model):
        title = models.TextField(
            verbose_name='Заголовок',
        )
        url = models.URLField(
            verbose_name='Ссылка'
        )
        user_name = models.TextField(
            verbose_name='Имя автора'
        )
        user_link = models.URLField(
            verbose_name='Ссылка на автора'
        )
        r_date = models.PositiveIntegerField(
            verbose_name='Дата публикации'
        )
        class Meta:
            verbose_name = 'Продукт'
            verbose_name_plural = 'Продукты'