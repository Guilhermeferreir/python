import googlemaps

def get_details_Local(api_key, address):
    gmaps = googlemaps.Client(key=api_key)

    try:
        result = gmaps.geocode(address)
        if result:
            local = result[0]
            name = local['formatted_address']
            latitude = local['geometry']['location']['lat']
            longitude = local['geometry']['location']['lng']
            
            print(f"name: {name}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
        else:
            print("No results found for the address provided.")

    except Exception as e:
        print(f"Error getting location details: {e}")

if __name__ == "__main__":
    key_api = ''

    address = ''

    get_details_Local(key_api, address)