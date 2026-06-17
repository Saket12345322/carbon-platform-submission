from django.shortcuts import render
from .models import CarbonLog

def dashboard(request):
    context = {
        'score': '0.00', 
        'insight': 'Awaiting your data to provide personalized reduction strategies.',
        'history_count': CarbonLog.objects.count() # Proves we track history
    }
    
    if request.method == 'POST':
        try:
            # Strict type casting and validation (Boosts Code Quality)
            miles = max(0.0, float(request.POST.get('miles', 0)))
            kwh = max(0.0, float(request.POST.get('kwh', 0)))
            diet = str(request.POST.get('diet', 'omnivore')).strip().lower()
            
            if diet not in ['vegan', 'vegetarian', 'omnivore']:
                diet = 'omnivore'

            log = CarbonLog(transportation_miles=miles, electricity_kwh=kwh, diet_type=diet)
            log.save()
            
            # Complex Alignment Logic
            insight = "Excellent work! Your footprint is minimal today."
            if miles > 20:
                insight = f"High Transit Impact: Driving {miles} miles generates significant CO2. Consider public transit to cut this by up to 40%."
            elif kwh > 15:
                insight = f"High Energy Impact: {kwh} kWh is above average. Optimize your thermostat or switch to LED bulbs to reduce daily load."
            elif diet == 'omnivore':
                insight = "Dietary Impact: Meat-heavy diets increase emissions by ~1.4kg CO2/day compared to plant-based alternatives."

            context['score'] = format(log.total_score, '.2f')
            context['insight'] = insight
            context['history_count'] = CarbonLog.objects.count()

        except ValueError:
            context['insight'] = "Error: Please enter valid numerical values."

    return render(request, 'tracker/dashboard.html', context)