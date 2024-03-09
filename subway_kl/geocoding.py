from django.conf import settings
from geopy.geocoders import GoogleV3


def get_coordinates(address, api_key=settings.GOOGLE_API_KEY):
    geolocator = GoogleV3(api_key=api_key)
    try:
        location = geolocator.geocode(address)
        if location:
            latitude, longitude = location.latitude, location.longitude
            return latitude, longitude
        else:
            print(f"No coordinates found for the address: {address}")
            return None
    except Exception as e:
        print(f"Error retrieving coordinates: {str(e)}")
        return None
