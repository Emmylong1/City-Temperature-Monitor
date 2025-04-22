import asyncio
import logging
import signal
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lib.temperature_scraper import scrape_temperatures

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def scheduled_scrape():
    """Run the temperature scraper"""
    logger.info("Running scheduled temperature scrape")
    
    try:
        results = await scrape_temperatures()
        logger.info(f"Successfully scraped temperatures for {len(results)} cities")
    except Exception as e:
        logger.error(f"Error during scheduled temperature scrape: {str(e)}")

async def main():
    """Main function to start the scheduler"""
    # Create scheduler
    scheduler = AsyncIOScheduler()
    
    # Add job to run every hour
    scheduler.add_job(scheduled_scrape, 'interval', hours=1)
    
    # Add job to run immediately on startup
    scheduler.add_job(scheduled_scrape, 'date')
    
    # Start scheduler
    scheduler.start()
    logger.info("Temperature scraper scheduler started")
    
    try:
        # Keep the scheduler running
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # Shutdown
        logger.info("Stopping temperature scraper scheduler...")
        scheduler.shutdown()

def signal_handler(sig, frame):
    """Handle SIGINT and SIGTERM signals"""
    logger.info("Shutting down temperature scraper scheduler...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the scheduler
    asyncio.run(main())
