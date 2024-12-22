import requests
from typing import List, Dict
from config.config import Config

class RouteService:
    @staticmethod
    def optimize_route(origin: str, destinations: List[str]) -> Dict:
        api_key = Config.GOOGLE_MAPS_API_KEY
        optimized_route = []
        total_distance = 0
        total_duration = 0

        try:
            for destination in destinations:
                url = f"https://maps.googleapis.com/maps/api/directions/json"
                params = {
                    'origin': origin,
                    'destination': destination,
                    'key': api_key
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                route_data = response.json()
                
                if route_data['status'] == 'OK':
                    leg = route_data['routes'][0]['legs'][0]
                    distance = leg['distance']
                    duration = leg['duration']
                    
                    optimized_route.append({
                        'destination': destination,
                        'distance': distance['text'],
                        'distance_value': distance['value'],
                        'duration': duration['text'],
                        'duration_value': duration['value'],
                        'steps': leg['steps']
                    })
                    
                    total_distance += distance['value']
                    total_duration += duration['value']
                    
            return {
                'routes': optimized_route,
                'total_distance': f"{total_distance/1000:.2f} km",
                'total_duration': f"{total_duration/3600:.2f} hours"
            }
            
        except requests.RequestException as e:
            raise Exception(f"Route optimization failed: {str(e)}")
