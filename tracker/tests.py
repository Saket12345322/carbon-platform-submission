from django.test import TestCase
from django.urls import reverse
from .models import CarbonLog

class CarbonTrackerTests(TestCase):
    def setUp(self):
        # Create a test log
        self.log = CarbonLog.objects.create(
            transportation_miles=20,
            electricity_kwh=10,
            diet_type='vegan'
        )

    def test_model_calculation(self):
        """Test if the carbon footprint math works correctly upon saving."""
        self.assertTrue(self.log.total_score > 0)
        self.assertEqual(self.log.diet_type, 'vegan')

    def test_dashboard_view(self):
        """Test if the dashboard loads with correct accessibility and status."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')