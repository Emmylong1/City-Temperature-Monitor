import aiohttp
import asyncio
import json
from datetime import datetime
import logging

from lib.db import insert_temperature, update_ipfs_hash
from lib.ipfs import store_on_ipfs
from lib.kafka import produce_to_kafka

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cities to scrape temperature data for
CITIES = ["Zurich", "London", "Miami", "Tokyo", "Singapore"]

async def fetch_temperature(city, session):
    """Fetch temperature data from wttr.in for a specific city"""
    try:
        # Using format=%t to get only the temperature
        url = f"https://wttr.in/{city}?format=%t"
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch temperature for {city}: {response.status}")
            
            data = await response.text()
            # Extract numeric temperature value from the response (e.g., "+20°C" -> 20)
            temperature = float(data.replace("°C", "").replace("+", "").strip())
            
            logger.info(f"{city}: {temperature}°C")
            return city, temperature
    except Exception as e:
        logger.error(f"Error fetching temperature for {city}: {str(e)}")
        raise

async def scrape_temperatures():
    """Scrape temperatures for all cities"""
    results = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city in CITIES:
            tasks.append(fetch_temperature(city, session))
        
        # Gather results, allowing individual cities to fail without stopping the whole process
        fetch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in fetch_results:
            if isinstance(result, Exception):
                logger.error(f"Failed to process city: {str(result)}")
                continue
                
            city, temperature = result
            timestamp = datetime.now().isoformat()
            
            # Create temperature record
            record = {
                "city": city,
                "temperature": temperature,
                "timestamp": timestamp
            }
            
            try:
                # Store in database
                id = await insert_temperature(city, temperature, timestamp)
                
                # Store on IPFS
                ipfs_hash = await store_on_ipfs(json.dumps(record))
                
                # Update record with IPFS hash
                await update_ipfs_hash(id, ipfs_hash)
                
                # Send to Kafka
                await produce_to_kafka("temperature-data", {
                    "id": id,
                    **record,
                    "ipfs_hash": ipfs_hash
                })
                
                results.append({
                    "id": id,
                    "city": city,
                    "temperature": temperature,
                    "timestamp": timestamp,
                    "ipfs_hash": ipfs_hash
                })
            except Exception as e:
                logger.error(f"Failed to process temperature for {city}: {str(e)}")
    
    return results
