from flask import jsonify, request
from flask_restful import Resource, reqparse
from app import api
import requests,os


#Define a class to get the temperature
class GetTemperature(Resource):

    def get(self):

        visitor_name = request.args.get('visitor_name')

        if not visitor_name:
            return jsonify({"message": "Name must be filled"})
        
         # Get requestor's IP address
        if request.headers.getlist("X-Forwarded-For"):
            ip_address = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip_address = request.remote_addr

         # IPinfo.io access token
        ipinfo_access_token = os.environ.get("IPNFO_KEY")

        # Get city information based on IP address (using ipinfo.io)
        ipinfo_url = f'https://ipinfo.io/{ip_address}/json?token={ipinfo_access_token}'

        response = requests.get(ipinfo_url)
        ipinfo_data = response.json()
        city = ipinfo_data.get('city')

        
        # Used OpenWeatherMap API to get weather information
        weather_api_key = os.environ.get("WEATHER_KEY")
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
        response = requests.get(weather_url)
        weather_data = response.json()
        weather = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']

        results= {
                "client_ip": f"{ip_address}", 
                "location": f"{city}",
                "greeting": f"'Hello, {visitor_name}!, the temperature is {temperature} in {city}"
                }

        return jsonify(results)

routes = [
    '/api/hello/',
]

api.add_resource(GetTemperature, *routes)