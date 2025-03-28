import time
import schedule
import threading
import requests
from flask import Flask, jsonify

from processor import process_temperature_data

app = Flask(__name__)
CITIES = ["Zurich", "London", "Miami", "Tokyo", "Singapore"]

# A global variable to store the latest temperatures.
temperature_data = {}

def fetch_temperature(city):
    """
    Fetch temperature data (in °C) from wttr.in for the given city.
    """
    url = f"http://wttr.in/{city}?format=%t"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"Failed to fetch data for {city}, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")
        return None

def job():
    """
    The scheduled job that runs every minute to fetch and process temperature data.
    """
    global temperature_data
    print("Fetching temperature data...")
    for city in CITIES:
        temperature = fetch_temperature(city)
        if temperature is not None:
            processed = process_temperature_data(city, temperature)
            temperature_data[city] = processed
            print(processed)
    print("Data fetched.\n")

def run_scheduler():
    """
    Function to run the scheduler.
    """
    # Run the job immediately on start
    job()
    # Schedule the job to run once every minute
    schedule.every(1).minutes.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/')
def home():
    """
    Return the latest temperature data as JSON.
    """
    return jsonify(temperature_data)

def main():
    # Run the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Start the Flask web server on port 5000
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
