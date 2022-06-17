from django.db import models


class OpenBasketManager(models.Manager):
    """Только для поиска, создания открытых корзин"""
    status_filter = "Open"

    def get_queryset(self):
        """Получить список открытых корзин"""
        return super().get_queryset().filter(
            status = self.status_filter)

    def get_or_create(self, **kwargs):
        """Получить или создать список открытых корзин"""
        return self.get_queryset().get_or_create(status=self.status_filter, **kwargs)


class SavedBasketManager(models.Manager):
    statys_filter = 'Saved'

    def get_queryset(self):
        return super().get_queryset().filter(
            status = self.status_filter)

    def create(self, **kwargs):
        return self.get_queryset().create(status=self.status_filter, **kwargs)

    def get_or_create(self, **kwargs):
        return self.get_queryset().get_or_create(status=self.status_filter, **kwargs)