import json
import requests
import requests_cache
from geopy.distance import vincenty

googleMapsAPIKey = "<YOUR GOOGLE MAPS API KEY>"

# Cache responses from reverse geocoding requests
requests_cache.install_cache("postcode_cache")

# Get GeoJSON coordinate-based representation of polygons representating postcode areas
polygons_string = open("polygons-original.geojson", "r").read()
polygons_json = json.loads(polygons_string)

# Find center coordinate of each polygon
for feature in polygons_json["features"]:
    x1 = float("inf")
    y1 = float("inf")
    x2 = float("-inf")
    y2 = float("-inf")

    coordinates = feature["geometry"]["coordinates"][0]

    for coordinate in coordinates:
        if coordinate[0] < y1:
            y1 = coordinate[0]

        if coordinate[1] < x1:
            x1 = coordinate[1]

        if coordinate[0] > y2:
            y2 = coordinate[0]

        if coordinate[1] > x2:
            x2 = coordinate[1]

    xCenter = x1 + ((x2 - x1) / 2)
    yCenter = y1 + ((y2 - y1) / 2)

    # Add center coordinates to properties of feature
    properties = feature["properties"]
    properties["centerCoordinates"] = {}
    centerCoordinates = properties["centerCoordinates"]
    centerCoordinates["lat"] = xCenter
    centerCoordinates["lng"] = yCenter

    # Calculate distance from center coordinates to coordinates along polygon edge furthest from the center
    furthestDistanceFromCenterToEdge = 0

    for coordinate in coordinates:
        distanceFromCenterToEdge = vincenty((xCenter, yCenter), (coordinate[1], coordinate[0])).meters

        if distanceFromCenterToEdge > furthestDistanceFromCenterToEdge:
            furthestDistanceFromCenterToEdge = distanceFromCenterToEdge

    # Add "radius" to properties of feature
    properties["approximateRadius"] = furthestDistanceFromCenterToEdge

    # Find postcode at each center coordinate
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(xCenter) + "," + str(yCenter) + "&key=" + googleMapsAPIKey
    response = requests.get(url)
    address_components = response.json()["results"][0]["address_components"]

    for address_component in address_components:
        if "postal_code" in address_component["types"]:
            # Add postcode to properties of feature
            properties["postcode"] = address_component["long_name"]

    # Print debug info when no postcode available
    if "postcode" not in properties:
        for address_component in address_components:
            print address_component["types"]

# Save modified GeoJSON to file
polygons_postcodes_file = open("polygons-postcodes.geojson", "w")
polygons_postcodes_file.write(json.dumps(polygons_json, sort_keys=True, indent=4))
