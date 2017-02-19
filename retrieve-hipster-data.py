import json
import requests
import requests_cache

# Cache responses from Foursquare requests
requests_cache.install_cache("hipster_data_cache")

# Get GeoJSON coordinate-based representation of polygons representating postcode areas
polygons_string = open("polygons-postcodes.geojson", "r").read()
polygons_json = json.loads(polygons_string)

# Create dictionary to count number of matching venues in each postcode area
venuesPerPostcode = {}

for feature in polygons_json["features"]:
    properties = feature["properties"]

    if "postcode" in properties:
        venuesPerPostcode[properties["postcode"]] = 0

# Find cafes in Berlin
url = "https://api.foursquare.com/v2/venues/search?near=Berlin&categoryId=4bf58dd8d48988d16d941735&v=20170216&client_id=HXU4QYFFBGG0DKWYY32L5AFKVW01DXO13W0ZQCXJJVOUVJR5&client_secret=QEMIIQVFGLHPKNYI3KYJKIVZUPYCIJ1LNX2A1THUGPTW5VX2"
response = requests.get(url)
venues = response.json()["response"]["venues"]

for venue in venues:
    postcode = venue["location"]["postalCode"]

    if postcode in venuesPerPostcode:
        # Add 1 to venue count for postcode
        venuesPerPostcode[postcode] += 1

# Print debug info to see roughly how many postcode areas contain venues
for postcode, venueCount in venuesPerPostcode.items():
    if venueCount > 0:
        print venueCount

for feature in polygons_json["features"]:
    properties = feature["properties"]

    if "postcode" in properties:
        # Add venue count to properties of feature
        properties["venueCount"] = venuesPerPostcode[properties["postcode"]]

# Save modified GeoJSON to file
polygons_string = json.dumps(polygons_json, sort_keys=True, indent=4)

polygons_postcodes_geojson_file = open("polygons-postcodes.geojson", "w")
polygons_postcodes_geojson_file.write(polygons_string)

# Save GeoJSON to JavaScript file
polygons_js_string = "var polygonsPostcodesGeoJSON = " + polygons_string + ";"

polygons_postcodes_js_file = open("polygons-postcodes-geojson.js", "w")
polygons_postcodes_js_file.write(polygons_js_string)
