from django.db import models
from django.core.validators import MinValueValidator


class Topping(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2,
                                validators=[MinValueValidator(0)])
    toppings = models.ManyToManyField(Topping)
    votes = models.IntegerField(default=0)

    def count_toppings(self):
        return self.toppings.count()

    def __str__(self):
        return self.name
