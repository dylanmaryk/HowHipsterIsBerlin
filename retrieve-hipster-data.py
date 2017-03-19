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

        approximateRadius = str(properties["approximateRadius"])

        postcode = properties["postcode"]

        properties["venueCount"] = 0
        venueCount = properties["venueCount"]

        venueIds = []

        # Find hipster locations around center of postcode area
        categoryIds = ["4bf58dd8d48988d179941735", # Bagel Shops
                       "4bf58dd8d48988d143941735", # Breakfast Spots
                       "52e81612bcbc57f1066b7a0c", # Bubble Tea Shops
                       "4bf58dd8d48988d16c941735", # Burger Joints
                       "4bf58dd8d48988d16d941735", # Cafes
                       "4bf58dd8d48988d1e0931735", # Coffee Shops
                       "52e81612bcbc57f1066b79f2", # Creperies
                       "4bf58dd8d48988d1d0941735", # Dessert Shops
                       "4bf58dd8d48988d148941735", # Donut Shop
                       "4bf58dd8d48988d120951735", # Food Courts
                       "56aa371be4b08b9a8d57350b", # Food Stands
                       "4bf58dd8d48988d1cb941735", # Food Trucks
                       "4c2cd86ed066bed06c3c5209", # Gluten-free Restaurants
                       "4bf58dd8d48988d112941735", # Juice Bars
                       "4bf58dd8d48988d1bd941735", # Salad Places
                       "4bf58dd8d48988d1c5941735", # Sandwich Places
                       "4bf58dd8d48988d1dc931735", # Tea Rooms
                       "52e81612bcbc57f1066b7a0d", # Beach Bars
                       "56aa371ce4b08b9a8d57356c", # Beer Bars
                       "4bf58dd8d48988d117941735", # Beer Gardens
                       "52e81612bcbc57f1066b7a0e", # Champagne Bars
                       "4bf58dd8d48988d11e941735", # Cocktail Bars
                       "4bf58dd8d48988d1d8941735", # Gay Bars
                       "4bf58dd8d48988d122941735", # Whisky Bars
                       "4bf58dd8d48988d123941735", # Wine Bars
                       "50327c8591d4c4b30a586d5d", # Breweries
                       "53e510b7498ebcb1801b55d4", # Night Markets
                       "4bf58dd8d48988d11f941735"] # Nightclubs

        for categoryId in categoryIds:
            url = "https://api.foursquare.com/v2/venues/search?ll=" + lat + "," + lng + "&radius=" + approximateRadius + "&intent=browse&categoryId=" + categoryId + "&limit=50&v=20170216&client_id=HXU4QYFFBGG0DKWYY32L5AFKVW01DXO13W0ZQCXJJVOUVJR5&client_secret=QEMIIQVFGLHPKNYI3KYJKIVZUPYCIJ1LNX2A1THUGPTW5VX2"
            response = requests.get(url)
            venues = response.json()["response"]["venues"]

            for venue in venues:
                location = venue["location"]
                venueId = venue["id"]

                if "postalCode" in location and location["postalCode"] == postcode and venueId not in venueIds:
                    # Add 1 to venue count for postcode if venue not already counted
                    venueCount += 1

                    venueIds.append(venueId)

        properties["venueCount"] = venueCount

# Save modified GeoJSON to file
polygons_string = json.dumps(polygons_json, sort_keys=True, indent=4)

polygons_postcodes_geojson_file = open("polygons-postcodes.geojson", "w")
polygons_postcodes_geojson_file.write(polygons_string)

# Save GeoJSON to JavaScript file
polygons_js_string = "var polygonsPostcodesGeoJSON = " + polygons_string + ";"

polygons_postcodes_js_file = open("polygons-postcodes-geojson.js", "w")
polygons_postcodes_js_file.write(polygons_js_string)
