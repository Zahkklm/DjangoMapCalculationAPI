import requests
import folium

def plot_route_on_map(start, finish, stations, route):
    """
    Plot the route and all fuel stations on an interactive map.
    
    Args:
        start: (latitude, longitude) of the starting point.
        finish: (latitude, longitude) of the destination point.
        stations: List of tuples [(lat, lon, price_per_gallon), ...].
        route: List of (lat, lon, price_per_gallon) representing the optimal route.
    """
    # Create a base map centered between start and finish
    mid_lat = (start[0] + finish[0]) / 2
    mid_lon = (start[1] + finish[1]) / 2
    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=6)

    # Add start point
    folium.Marker(location=start, popup="Start", icon=folium.Icon(color="green")).add_to(m)

    # Add finish point
    folium.Marker(location=finish, popup="Finish", icon=folium.Icon(color="red")).add_to(m)

    # Add all fuel stations
    for lat, lon, price in stations:
        folium.CircleMarker(
            location=(lat, lon),
            radius=5,
            color="blue",
            fill=True,
            fill_opacity=0.7,
            popup=f"Price: ${price}/gallon"
        ).add_to(m)

    # Plot the route
    route_coords = [(lat, lon) for lat, lon, _ in route]
    folium.PolyLine(route_coords, color="orange", weight=5, opacity=0.8, popup="Optimal Route").add_to(m)

    # Show the map
    return m

def main():
    # Define the start and end coordinates
    start_lat = 40.7128
    start_lng = -74.0060
    end_lat = 34.0522
    end_lng = -118.2437

    # Send GET request to the route endpoint
    url = f"http://localhost:8000/route/?start_lat={start_lat}&start_lng={start_lng}&end_lat={end_lat}&end_lng={end_lng}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to get route data: {response.status_code}")
        return

    # Parse the JSON response
    data = response.json()
    total_cost = data['total_cost']
    fuel_stops = data['fuel_stops']
    map_url = data['map_url']

    # Extract start and finish points
    start = (start_lat, start_lng)
    finish = (end_lat, end_lng)

    # Extract stations and route
    stations = [(stop['lat'], stop['lng'], stop['price_per_gallon']) for stop in fuel_stops]
    route = [(stop['lat'], stop['lng'], 0) for stop in fuel_stops]

    # Generate the map
    map_result = plot_route_on_map(start, finish, stations, route)
    map_result.save("map.html")
    print(f"Map saved to map.html with total cost: ${total_cost}")

if __name__ == "__main__":
    main()