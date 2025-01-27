# Django API for Route Optimization

This project is a Django-based API that calculates optimal fueling locations along a route in the USA based on user-defined start and finish locations. It takes into account fuel prices and vehicle range to provide cost-effective fueling options.

## Features

- Accepts start and finish locations within the USA.
- Calculates the route and identifies optimal fueling locations based on fuel prices.
- Assumes a vehicle range of 500 miles and fuel efficiency of 10 miles per gallon.
- Returns total money spent on fuel for the trip.

## Requirements

- Python 3.6 or higher
- Django 3.2.23
- Additional dependencies listed in `requirements.txt`

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd django-api
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- **POST /api/route/**
  - Description: Calculate the optimal route and fueling locations.
  - Request Body: JSON containing `start_location` and `finish_location`.
  - Response: JSON with route details and fueling locations.

## Testing

To run the tests, use the following command:
```
python manage.py test
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.