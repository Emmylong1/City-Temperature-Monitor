import os
import json
import asyncio
import logging
import signal
import sys

from lib.db import get_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def process_message(message):
    """Process a message from Kafka"""
    try:
        # Parse message
        data = json.loads(message.value().decode('utf-8'))
        logger.info(f"Received temperature data from Kafka: {data}")
        
        # Get database connection
        conn = await get_connection()
        try:
            # Check if the record already exists in the database
            row = await conn.fetchrow("SELECT id FROM temperatures WHERE id = $1", data['id'])
            
            if row is None:
                # Insert the record if it doesn't exist
                await conn.execute(
                    """
                    INSERT INTO temperatures (id, city, temperature, timestamp, ipfs_hash) 
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    data['id'], data['city'], data['temperature'], data['timestamp'], data['ipfs_hash']
                )
                logger.info(f"Stored temperature data for {data['city']} in database")
            else:
                logger.info(f"Temperature data for {data['city']} already exists in database")
        finally:
            await conn.close()
    except Exception as e:
        logger.error(f"Error processing temperature data from Kafka: {str(e)}")

async def start_temperature_consumer():
    """Start the Kafka consumer for temperature data"""
    try:
        # Check if confluent_kafka is available
        try:
            from confluent_kafka import Consumer, KafkaError
            
            # Kafka connection parameters
            KAFKA_BROKERS = os.environ.get("KAFKA_BROKERS", "localhost:9092")
            
            # Kafka consumer configuration
            consumer_config = {
                'bootstrap.servers': KAFKA_BROKERS,
                'group.id': 'temperature-consumer-group',
                'auto.offset.reset': 'latest',
                'enable.auto.commit': True
            }
            
            # Create consumer
            consumer = Consumer(consumer_config)
            
            # Subscribe to topics
            consumer.subscribe(['temperature-data'])
            
            logger.info("Temperature data consumer started")
            
            # Process messages
            running = True
            while running:
                try:
                    # Poll for messages
                    msg = consumer.poll(1.0)
                    
                    if msg is None:
                        # No message received
                        continue
                    
                    if msg.error():
                        # Error
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            # End of partition event
                            logger.info(f"Reached end of partition {msg.partition()}")
                        else:
                            # Error
                            logger.error(f"Consumer error: {msg.error()}")
                        continue
                    
                    # Process message
                    await process_message(msg)
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
            
            # Close consumer
            consumer.close()
        except ImportError:
            logger.warning("confluent_kafka not installed, running mock consumer")
            while True:
                logger.info("Mock Kafka consumer running...")
                await asyncio.sleep(60)
    except Exception as e:
        logger.error(f"Error starting temperature data consumer: {str(e)}")

def signal_handler(sig, frame):
    """Handle SIGINT and SIGTERM signals"""
    logger.info("Shutting down temperature data consumer...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the consumer
    asyncio.run(start_temperature_consumer())
