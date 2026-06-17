from django.test import TestCase, Client
from django.urls import reverse
from .models import CarbonLog

class CarbonTrackerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_model_calculation_omnivore(self):
        """Test valid footprint calculation."""
        log = CarbonLog.objects.create(transportation_miles=10, electricity_kwh=5, diet_type='omnivore')
        expected = round((10 * 0.404) + (5 * 0.385) + 2.5, 2)
        self.assertEqual(log.total_score, expected)

    def test_model_calculation_vegan(self):
        """Test footprint logic branches."""
        log = CarbonLog.objects.create(transportation_miles=0, electricity_kwh=0, diet_type='vegan')
        self.assertEqual(log.total_score, 1.1)

    def test_view_get_request(self):
        """Test dashboard accessibility and load status."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/dashboard.html')

    def test_view_post_valid_data(self):
        """Test complete user flow."""
        response = self.client.post(reverse('dashboard'), {
            'miles': '20',
            'kwh': '10',
            'diet': 'vegetarian'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total Footprint')

    def test_view_post_invalid_data(self):
        """Test edge cases and invalid input handling."""
        response = self.client.post(reverse('dashboard'), {
            'miles': 'invalid_string',
            'kwh': '-5',
            'diet': 'unknown'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Error')