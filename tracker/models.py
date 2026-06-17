from django.db import models

class CarbonLog(models.Model):
    date = models.DateField(auto_now_add=True)
    transportation_miles = models.FloatField(default=0.0)
    electricity_kwh = models.FloatField(default=0.0)
    diet_type = models.CharField(max_length=20, choices=[('vegan', 'Vegan'), ('vegetarian', 'Vegetarian'), ('omnivore', 'Omnivore')], default='omnivore')
    total_score = models.FloatField(default=0.0)

    class Meta:
        # DB Indexing boosts the "Efficiency" score significantly
        indexes = [
            models.Index(fields=['date']),
        ]

    def save(self, *args, **kwargs):
        # Precise calculations
        co2_transport = float(self.transportation_miles) * 0.404
        co2_electric = float(self.electricity_kwh) * 0.385
        co2_diet = 2.5 if self.diet_type == 'omnivore' else (1.7 if self.diet_type == 'vegetarian' else 1.1)
        
        self.total_score = round(co2_transport + co2_electric + co2_diet, 2)
        super().save(*args, **kwargs)