# filepath: /c:/Users/zagor/Documents/django-api/api/views.py
import csv
import logging
import polyline
import requests
import numpy as np
from scipy.spatial import KDTree
from geopy.distance import great_circle
from django.http import JsonResponse
from django.views import View
import folium
from visualize_map import plot_route_on_map
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class RouteView(View):
    GEOAPIFY_API_KEY = os.getenv('GEOAPIFY_API_KEY')
    ORS_API_KEY = os.getenv('ORS_API_KEY')

    MAX_RANGE = 500  # miles
    MPG = 10

    def __init__(self):
        super().__init__()
        self.fuel_stations = self._load_fuel_stations()
        
    def _load_fuel_stations(self):
        """Load fuel stations from CSV and build spatial index"""
        stations = []
        coords = []
        try:
            with open('fuelprices_HERE_geocoded.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        lat = float(row['Latitude'])
                        lng = float(row['Longitude'])
                        price = float(row['Retail Price'])
                        stations.append({'lat': lat, 'lng': lng, 'price': price})
                        coords.append([lat, lng])
                    except (KeyError, ValueError) as e:
                        logger.warning(f"Invalid station data: {e}")
                        continue
            return {
                'stations': stations,
                'tree': KDTree(coords) if coords else None
            }
        except Exception as e:
            logger.error(f"Failed loading fuel data: {e}")
            return {'stations': [], 'tree': None}

    def get(self, request):
        # Validate parameters
        try:
            start_lat = float(request.GET['start_lat'])
            start_lng = float(request.GET['start_lng'])
            end_lat = float(request.GET['end_lat'])
            end_lng = float(request.GET['end_lng'])
        except (KeyError, ValueError):
            return JsonResponse({'error': 'Invalid/missing coordinates'}, status=400)

        # Get route geometry from OpenRouteService
        route_data = self._get_route_geometry(start_lng, start_lat, end_lng, end_lat)
        if not route_data:
            return JsonResponse({'error': 'Route calculation failed'}, status=500)

        # Find fuel stations along route
        fuel_stops, total_cost = self._calculate_fuel_stops(route_data['coordinates'], 
                                                          route_data['total_miles'])
        if not fuel_stops:
            return JsonResponse({'error': 'No fuel stations found along route'}, status=500)

        # Generate map using visualize_map.py
        start = (start_lat, start_lng)
        finish = (end_lat, end_lng)
        stations = [(stop['lat'], stop['lng'], stop['price_per_gallon']) for stop in fuel_stops]
        route = [(coord[1], coord[0], 0) for coord in route_data['coordinates']]  # Note: coord[1] is lat, coord[0] is lng

        map_result = plot_route_on_map(start, finish, stations, route)
        map_result.save("map.html")

        return JsonResponse({
            'total_cost': round(total_cost, 2),
            'fuel_stops': fuel_stops,
            'map_url': "map.html"
        })

    def _get_route_geometry(self, start_lng, start_lat, end_lng, end_lat):
        """Get route data from OpenRouteService API"""
        try:
            url = "https://api.openrouteservice.org/v2/directions/driving-car"
            headers = {
                'Authorization': self.ORS_API_KEY,
                'Content-Type': 'application/json'
            }
            payload = {
                "coordinates": [
                    [start_lng, start_lat],
                    [end_lng, end_lat]
                ]
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                return None
            
            data = response.json()
            geometry = polyline.decode(data['routes'][0]['geometry'])
            total_miles = data['routes'][0]['summary']['distance'] / 1609.34
            
            return {
                'coordinates': geometry,
                'total_miles': total_miles,
                'polyline': data['routes'][0]['geometry']
            }
        except Exception as e:
            logger.error(f"Routing error: {e}")
            return None

    def _calculate_fuel_stops(self, route_coords, total_distance):
        """Calculate optimal fuel stops along route"""
        stops = []
        total_cost = 0.0
        route_points = self._create_route_points(route_coords)
        route_tree = KDTree([[p['lat'], p['lng']] for p in route_points])

        current_pos = 0.0
        while current_pos < total_distance:
            max_range = min(current_pos + self.MAX_RANGE, total_distance)
            print(f"Current position: {current_pos} miles, max range: {max_range} miles")
            # Find station candidates in current segment
            candidates = []
     
            for station in self.fuel_stations['stations']:
                # Find nearest point on route
                _, idx = route_tree.query([[station['lat'], station['lng']]])
                print(f"Nearest route point index: {idx}")
                idx = int(idx)  # Ensure idx is an integer
                route_point = route_points[idx]
                print(f"Nearest route point: {route_point}")
                
                logger.debug(f"Checking station at ({station['lat']}, {station['lng']}) with price {station['price']}")
                logger.debug(f"Nearest route point at ({route_point['lat']}, {route_point['lng']}) with mile position {route_point['mile_position']}")
                print(f"Checking station at ({station['lat']}, {station['lng']}) with price {station['price']}")

                if current_pos <= route_point['mile_position'] <= max_range:
                    distance_from_route = great_circle(
                        (station['lat'], station['lng']),
                        (route_point['lat'], route_point['lng'])
                    ).miles
                    
                    logger.debug(f"Distance from route: {distance_from_route} miles")
                    print(f"Distance from route: {distance_from_route} miles")
                    if distance_from_route >= 0:  # Max 100 miles off-route
                        candidates.append({
                            **station,
                            'mile_position': route_point['mile_position'],
                            'distance_from_route': distance_from_route
                        })

            if not candidates:
                logger.warning(f"No stations found in range for segment starting at {current_pos} miles")
                return None, 0  # No stations in range

            # Select cheapest station in segment
            cheapest = min(candidates, key=lambda x: x['price'])
            segment_distance = cheapest['mile_position'] - current_pos
            total_cost += (segment_distance / self.MPG) * cheapest['price']
            stops.append({
                'lat': cheapest['lat'],
                'lng': cheapest['lng'],
                'price_per_gallon': cheapest['price'],
                'distance_from_start': round(cheapest['mile_position'], 1)
            })
            
            current_pos = cheapest['mile_position'] + (self.MAX_RANGE - 10)  # Conservative buffer

        return stops, total_cost

    def _create_route_points(self, coordinates):
        """Create route points with cumulative mileage"""
        points = []
        cumulative_miles = 0.0
        prev = None
        
        for coord in coordinates:
            if prev:
                segment = great_circle(prev, coord).miles
                cumulative_miles += segment
                
            points.append({
                'lat': coord[0],  # Note: coord[1] is latitude, coord[0] is longitude
                'lng': coord[1],
                'mile_position': cumulative_miles
            })
            prev = coord
            
        return points