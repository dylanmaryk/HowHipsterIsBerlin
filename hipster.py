import json
import requests
import requests_cache

# Cache responses from reverse geocoding requests
requests_cache.install_cache("hipster_cache")

# Get GeoJSON coordinate-based representation of polygons representating postcode areas
polygons_string = open("postcodes.geojson", "r").read()
polygons_json = json.loads(polygons_string)

# Find center coordinate of each polygon
for feature in polygons_json["features"]:
    x1 = float("inf")
    y1 = float("inf")
    x2 = float("-inf")
    y2 = float("-inf")

    coordinates = feature["geometry"]["coordinates"][0]

    for coordinate in coordinates:
        if coordinate[0] < x1:
            x1 = coordinate[0]

        if coordinate[1] < y1:
            y1 = coordinate[1]

        if coordinate[0] > x2:
            x2 = coordinate[0]

        if coordinate[1] > y2:
            y2 = coordinate[1]

    xCenter = x1 + ((x2 - x1) / 2)
    yCenter = y1 + ((y2 - y1) / 2)

    # Find postcode at each center coordinate
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(yCenter) + "," + str(xCenter) + "&key=AIzaSyCLus9zsDqpQ50kW_A5oafRhUXXI2kxuw8"
    response = requests.get(url)
    address_components = response.json()["results"][0]["address_components"]

    for address_component in address_components:
        if "postal_code" in address_component["types"]:
            print address_component["long_name"] # Add to feature["properties"]

# Convert JSON to string
# Save string to file
