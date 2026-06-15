from django.shortcuts import render
from .models import CarbonLog

def dashboard(request):
    context = {'score': 0.00, 'insight': 'Enter your daily data to see your impact.'}
    
    if request.method == 'POST':
        # Grab data from the HTML form
        miles = float(request.POST.get('miles', 0))
        kwh = float(request.POST.get('kwh', 0))
        diet = request.POST.get('diet', 'omnivore')
        
        # Save to database (This fixes the 'Tracking' requirement)
        log = CarbonLog(transportation_miles=miles, electricity_kwh=kwh, diet_type=diet)
        log.save()
        
        # Generate personalized insights
        insight = "Great job!"
        if miles > 15:
            insight = "Actionable Insight: Try carpooling or taking public transit twice a week to cut your transport emissions by 20%."
        elif diet == 'omnivore':
            insight = "Actionable Insight: Swapping just one meat-based meal for a plant-based one today saves roughly 1.5 kg of CO2."
        elif kwh > 10:
            insight = "Actionable Insight: Unplugging idle electronics can reduce your daily electricity footprint."
            
        context['score'] = round(log.total_score, 2)
        context['insight'] = insight

    return render(request, 'dashboard.html', context)