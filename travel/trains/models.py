from django.db import models
from django.core.exceptions import ValidationError
from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Number train')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                        verbose_name='Starting station',
                                        related_name = 'from_city')

    to_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                        verbose_name='End station',
                                        related_name = 'to_city')

    travel_time = models.IntegerField(verbose_name='Travel time')

    class Meta:
        verbose_name = 'Train'
        verbose_name_plural = 'Trains'
        #ordering = ['name']

    def __str__(self):
        return 'Train №{} from {} in {} '.format(self.name, self.from_city, self.to_city)

    def clean(self, *args, **kwargs):
        if self.from_city == self.to_city:
            raise ValidationError("The city of departure cannot match the city of arrival")
        qs = Train.objects.filter(from_city=self.from_city,
                                  to_city=self.to_city,
                                  travel_time=self.travel_time).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Train with same data already exist")
        return super(Train, self).clean(*args, **kwargs)