from django.db import models
from trains.models import Train

class Route(models.Model):
    name = models.CharField(max_length=100, verbose_name='Route name', unique=True)
    from_city = models.CharField(max_length=100, verbose_name='From')
    to_city = models.CharField(max_length=100, verbose_name='To')
    across_cities = models.ManyToManyField(Train, blank=True, verbose_name='Across City')
    travel_times = models.IntegerField(verbose_name='Travel time')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'
