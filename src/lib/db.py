import os
import asyncpg
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database connection parameters
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "temperature_db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_SSL = os.environ.get("DB_SSL", "false").lower() == "true"

async def get_connection():
    """Get a database connection"""
    return await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        ssl="require" if DB_SSL else None
    )

async def check_db_connection():
    """Check if the database connection is working"""
    conn = await get_connection()
    try:
        await conn.execute("SELECT 1")
    finally:
        await conn.close()

async def init_schema():
    """Initialize the database schema"""
    try:
        conn = await get_connection()
        try:
            # Create temperatures table if it doesn't exist
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS temperatures (
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(100) NOT NULL,
                    temperature DECIMAL(5,2) NOT NULL,
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    ipfs_hash VARCHAR(100)
                )
            """)
            
            # Create index on city and timestamp for faster queries
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_city_timestamp ON temperatures (city, timestamp)
            """)
            
            logger.info("Database schema initialized successfully")
        finally:
            await conn.close()
    except Exception as e:
        logger.error(f"Error initializing database schema: {str(e)}")
        raise

async def insert_temperature(city, temperature, timestamp):
    """Insert temperature data into the database"""
    conn = await get_connection()
    try:
        result = await conn.fetchval(
            "INSERT INTO temperatures (city, temperature, timestamp) VALUES ($1, $2, $3) RETURNING id",
            city, temperature, timestamp
        )
        return result
    finally:
        await conn.close()

async def update_ipfs_hash(id, ipfs_hash):
    """Update the IPFS hash for a temperature record"""
    conn = await get_connection()
    try:
        await conn.execute(
            "UPDATE temperatures SET ipfs_hash = $1 WHERE id = $2",
            ipfs_hash, id
        )
    finally:
        await conn.close()

async def get_temperatures(limit=1000):
    """Get temperature data from the database"""
    try:
        conn = await get_connection()
        try:
            rows = await conn.fetch(
                """
                SELECT id, city, temperature, timestamp::text, ipfs_hash 
                FROM temperatures 
                ORDER BY timestamp DESC 
                LIMIT $1
                """,
                limit
            )
            # Convert rows to dictionaries
            return [dict(row) for row in rows]
        finally:
            await conn.close()
    except Exception as e:
        logger.error(f"Error getting temperatures: {str(e)}")
        # If database is not available, return mock data
        return generate_mock_data()

def generate_mock_data():
    """Generate mock temperature data for development and testing"""
    logger.warning("Generating mock temperature data")
    data = []
    cities = ["Zurich", "London", "Miami", "Tokyo", "Singapore"]
    
    # Generate data for the last 24 hours
    now = datetime.now()
    
    for i in range(100):
        city = cities[i % len(cities)]
        timestamp = now.replace(hour=now.hour - (i % 24), minute=0, second=0, microsecond=0)
        
        # Generate a realistic temperature for each city
        base_temp = {
            "Zurich": 15,
            "London": 12,
            "Miami": 28,
            "Tokyo": 20,
            "Singapore": 30
        }.get(city, 20)
        
        # Add some random variation
        import random
        temperature = round(base_temp + (random.random() * 6 - 3), 1)
        
        data.append({
            "id": i + 1,
            "city": city,
            "temperature": temperature,
            "timestamp": timestamp.isoformat(),
            "ipfs_hash": f"mock-ipfs-hash-{i}"
        })
    
    return data
