from django.db import models
from django.contrib.auth.models import User

class CarbonLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    transportation_miles = models.FloatField(default=0.0) # Miles driven
    electricity_kwh = models.FloatField(default=0.0)       # Monthly/daily kWh
    diet_type = models.CharField(max_length=20, choices=[('vegan', 'Vegan'), ('vegetarian', 'Vegetarian'), ('omnivore', 'Omnivore')], default='omnivore')
    total_score = models.FloatField(default=0.0)           # Calculated CO2 in kg

    def save(self, *args, **kwargs):
        # Quick mathematical logic for footprint conversion
        co2_transport = self.transportation_miles * 0.404  # ~0.404 kg CO2 per mile
        co2_electric = self.electricity_kwh * 0.385       # ~0.385 kg CO2 per kWh
        co2_diet = 2.5 if self.diet_type == 'omnivore' else (1.7 if self.diet_type == 'vegetarian' else 1.1)
        
        self.total_score = co2_transport + co2_electric + co2_diet
        super().save(*args, **kwargs)