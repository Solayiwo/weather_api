import requests
from django.http import JsonResponse
from django.conf import settings


api_key = settings.WEATHER_API_KEY


def get_client_ip(request):
    """Retrieve the client's IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(ip):
    """Retrieve the location based  on the client's IP address,
        using ipinfo service to get the location
    """
    ip_api_url = f'https://ipinfo.io/{ip}/json'
    response = requests.get(ip_api_url)
    ip_data = response.json()

    return ip_data.get("city", "City name")

def get_weather(city):
    "Retrieve the weather information for the given city by the IP"
    wx_api_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    response = requests.get(wx_api_url)
    wx_data = response.json()

    return wx_data["current"]["temp_c"]

def greeting_msg(request):
    """APi endpoint to return a greeting with weather information"""
    visitor_name = request.GET.get('visitor_name', 'vistor')
    client_ip = get_client_ip(request)
    location = get_location(client_ip)
    temperature = get_weather(location)

    response_data = {
        "client_ip": client_ip,
        "location": location,
        "greeting": "Hello, {}!, the temperature is {} degrees \
Celsius in {}".format(visitor_name, temperature, location)
    }

    return JsonResponse(response_data)

