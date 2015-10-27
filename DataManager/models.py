from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100, )
    forms = models.CharField(max_length=1000)   # comma-separated forms of country name ex. Polska, Polski, Polsce


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(to='Country', to_field='id')
    forms = models.CharField(max_length=1000)


class Airline(models.Model):
    name = models.CharField(max_length=50)
    forms = models.CharField(max_length=1000)
