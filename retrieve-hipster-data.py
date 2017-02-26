import json
import requests
import requests_cache

# Cache responses from Foursquare requests
requests_cache.install_cache("hipster_data_cache")

# Get GeoJSON coordinate-based representation of polygons representating postcode areas
polygons_string = open("polygons-postcodes.geojson", "r").read()
polygons_json = json.loads(polygons_string)

for feature in polygons_json["features"]:
    properties = feature["properties"]

    if "postcode" in properties:
        centerCoordinates = properties["centerCoordinates"]
        lat = str(centerCoordinates["lat"])
        lng = str(centerCoordinates["lng"])

        postcode = properties["postcode"]

        properties["venueCount"] = 0
        venueCount = properties["venueCount"]

        # Find cafes around center of postcode area
        url = "https://api.foursquare.com/v2/venues/search?ll=" + lat + "," + lng + "&radius=5000&intent=browse&categoryId=4bf58dd8d48988d16d941735&limit=50&v=20170216&client_id=HXU4QYFFBGG0DKWYY32L5AFKVW01DXO13W0ZQCXJJVOUVJR5&client_secret=QEMIIQVFGLHPKNYI3KYJKIVZUPYCIJ1LNX2A1THUGPTW5VX2"
        response = requests.get(url)
        venues = response.json()["response"]["venues"]

        for venue in venues:
            location = venue["location"]

            if "postalCode" in location:
                if location["postalCode"] == postcode:
                    # Add 1 to venue count for postcode
                    venueCount += 1

        properties["venueCount"] = venueCount

# Save modified GeoJSON to file
polygons_string = json.dumps(polygons_json, sort_keys=True, indent=4)

polygons_postcodes_geojson_file = open("polygons-postcodes.geojson", "w")
polygons_postcodes_geojson_file.write(polygons_string)

# Save GeoJSON to JavaScript file
polygons_js_string = "var polygonsPostcodesGeoJSON = " + polygons_string + ";"

polygons_postcodes_js_file = open("polygons-postcodes-geojson.js", "w")
polygons_postcodes_js_file.write(polygons_js_string)
