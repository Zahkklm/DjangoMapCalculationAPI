from django.test import TestCase
from django.urls import reverse

class APITests(TestCase):
    def test_route_endpoint(self):
        response = self.client.get(reverse('route_endpoint'))  # Replace 'route_endpoint' with your actual endpoint name
        self.assertEqual(response.status_code, 200)
        self.assertIn('route', response.json())  # Check if 'route' is in the response

    def test_fuel_price_calculation(self):
        start_location = "Location A"
        finish_location = "Location B"
        response = self.client.post(reverse('route_endpoint'), data={
            'start': start_location,
            'finish': finish_location
        })  # Replace 'route_endpoint' with your actual endpoint name
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_cost', response.json())  # Check if 'total_cost' is in the response

    def test_multiple_fuel_stops(self):
        start_location = "Location A"
        finish_location = "Location B"
        response = self.client.post(reverse('route_endpoint'), data={
            'start': start_location,
            'finish': finish_location
        })  # Replace 'route_endpoint' with your actual endpoint name
        self.assertEqual(response.status_code, 200)
        self.assertIn('fuel_stops', response.json())  # Check if 'fuel_stops' is in the response

    # Add more tests as needed for your application logic