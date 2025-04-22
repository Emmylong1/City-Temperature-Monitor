import os
import json
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Kafka connection parameters
KAFKA_BROKERS = os.environ.get("KAFKA_BROKERS", "localhost:9092")

async def produce_to_kafka(topic, message):
    """Send message to Kafka topic"""
    try:
        # Check if confluent_kafka is available
        try:
            from confluent_kafka import Producer
            
            # Kafka producer configuration
            producer_config = {
                'bootstrap.servers': KAFKA_BROKERS,
                'client.id': 'temperature-service-producer'
            }
            
            # Create producer
            producer = Producer(producer_config)
            
            # Convert message to JSON
            value = json.dumps(message).encode('utf-8')
            
            # Delivery report callback
            def delivery_report(err, msg):
                if err is not None:
                    logger.error(f"Message delivery failed: {err}")
                else:
                    logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
            
            # Produce message
            producer.produce(topic, value=value, callback=delivery_report)
            
            # Flush to ensure message is sent
            producer.flush()
            
            logger.info(f"Message sent to Kafka topic {topic}")
        except ImportError:
            logger.warning("confluent_kafka not installed, skipping Kafka message")
            logger.info(f"Would have sent to Kafka topic {topic}: {message}")
    except Exception as e:
        logger.error(f"Error sending message to Kafka topic {topic}: {str(e)}")
