from django.db import models

class FuelPrice(models.Model):
    location = models.CharField(max_length=255)
    price_per_gallon = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.location}: ${self.price_per_gallon}/gallon"

class Route(models.Model):
    start_location = models.CharField(max_length=255)
    finish_location = models.CharField(max_length=255)
    distance = models.FloatField()  # Distance in miles
    fuel_stops = models.ManyToManyField(FuelPrice, related_name='routes')

    def __str__(self):
        return f"Route from {self.start_location} to {self.finish_location}"