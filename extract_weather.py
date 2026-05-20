import requests
import json
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd

cities = [
    {"name": "Cairo", "latitude": 30.0444, "longitude": 31.2357},
    {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
    {"name": "New York", "latitude": 40.7128, "longitude": -74.0060},
    {"name": "Tokyo", "latitude": 35.6762, "longitude": 139.6503},
    {"name": "Sydney", "latitude": -33.8688, "longitude": 151.2093}
]

def get_weather(latitude, longitude):
    """
    Fetch current weather from open-meteo API
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

    try:
        respone = requests.get(url, timeout=10)
        #to seen the response 200 or 400 or 500 or 404 or anything else
        respone.raise_for_status()
        #it catches connection errors or timeout
        return respone.json()
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None
   
def load_to_postgres(data_list):
    """
    Load weather data to PostgreSQL using pandas + SQLAlchemy
    """
    try:
        # Create connection engine
        # Format: postgresql://username:password@host:port/database
        engine = create_engine('postgresql://weather:weather@localhost:5433/weather_db')
        
        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(data_list)
        
        # Rename 'timestamp' column to avoid conflict with SQL keyword
        df = df.rename(columns={'timestamp': 'weather_timestamp'})
        
        # Load to database
        # if_exists='append': add to existing data
        # index=False: don't save DataFrame index as a column
        df.to_sql('raw_weather', engine, if_exists='append', index=False)
        
        print(f"Successfully loaded {len(df)} records to PostgreSQL")
        return True
        
    except Exception as e:
        print(f"Error loading to PostgreSQL: {e}")
        return False
    
def main():
    print("=" *50)
    print("WEATHER DATA EXTRACTION")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" *50)
    all_weather_data = []

    for city in cities:
        print(f"\nFetching weather for {city['name']}...")

        weather_data = get_weather(city['latitude'], city['longitude'])

        if weather_data and 'current_weather' in weather_data:
            current = weather_data['current_weather']

            record = {
                'city': city['name'],
                'latitude': city['latitude'],
                'longitude': city['longitude'],
                'temperature': current['temperature'],
                'windspeed': current['windspeed'],
                'winddirection': current['winddirection'],
                'weathercode': current['weathercode'],
                'timestamp': datetime.now().isoformat()
            }

            all_weather_data.append(record)

            print(f"  Temperature: {current['temperature']}°C")
            print(f"  Wind Speed: {current['windspeed']} km/h")
        else:
            print(f"  FAILED to get data for {city['name']}")
    
    # Save to JSON file
    output_file = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w') as f:
        json.dump(all_weather_data, f, indent=2)
    
    print("\n" + "=" * 50)
    print(f"Saved {len(all_weather_data)} records to {output_file}")
    # NEW: Load to PostgreSQL
    postgres_success = load_to_postgres(all_weather_data)
    
    if postgres_success:
        print(f"Loaded {len(all_weather_data)} records to PostgreSQL")
    else:
        print("WARNING: PostgreSQL load failed, but JSON backup saved")
    
    print("=" * 50)


if __name__ == "__main__":
    main()