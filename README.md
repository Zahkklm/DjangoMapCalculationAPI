# Django API for Route Optimization

This project is a Django-based API that calculates optimal fueling locations along a route in the USA based on user-defined start and finish locations. It takes into account fuel prices and vehicle range to provide cost-effective fueling options.

## Features

- Accepts start and finish locations within the USA.
- Calculates the route and identifies optimal fueling locations based on fuel prices.
- Assumes a vehicle range of 500 miles and fuel efficiency of 10 miles per gallon.
- Returns total money spent on fuel for the trip.
- Generates an interactive map showing the route and fueling locations.

## Requirements

- Python 3.6 or higher
- Django 3.2.23
- Additional dependencies listed in `requirements.txt`

## Setup Instructions

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd django-api
   ```

2. Install the required packages:
   ```pip install -r requirements.txt```

3. Create a .env file in the root directory and add your API keys:

```
GEOAPIFY_API_KEY=your_geoapify_api_key
ORS_API_KEY=your_openrouteservice_api_key
```

4. Run database migrations:

```python manage.py migrate```

5. Start the development server:

## API Endpoints

- **GET /route/**

  - **Description**: Calculate the optimal route and fueling locations.
  - **Query Parameters**:
    - `start_lat`: Latitude of the starting location.
    - `start_lng`: Longitude of the starting location.
    - `end_lat`: Latitude of the ending location.
    - `end_lng`: Longitude of the ending location.
  - **Response**: JSON with route details, fueling locations, and a URL to the generated map.

  Example request:
  ```sh
  curl -X GET "http://localhost:8000/route/?start_lat=40.7128&start_lng=-74.0060&end_lat=34.0522&end_lng=-118.2437"

Example response:

```json
{
  "total_cost": 187.9,
  "fuel_stops": [
    {"lat": 38.76086, "lng": -78.6314, "price_per_gallon": 2.899, "distance_from_start": 257.6},
    {"lat": 30.24119, "lng": -92.17626, "price_per_gallon": 2.98233333, "distance_from_start": 925.7},
    {"lat": 30.8045, "lng": -97.61614, "price_per_gallon": 2.919, "distance_from_start": 1420.1},
    {"lat": 35.35359, "lng": -109.05351, "price_per_gallon": 3.299, "distance_from_start": 2077.6},
    {"lat": 32.67038, "lng": -114.44936, "price_per_gallon": 3.489, "distance_from_start": 2577.8}
  ],
  "map_url": "map.html"
}
```

Testing
To run the tests, use the following command:

```
python manage.py test
```
