from django.db import models


class Home(models.Model):
    temperature = models.DecimalField( max_digits=4, decimal_places=2)
    humidity = models.DecimalField(max_digits=4, decimal_places=2)