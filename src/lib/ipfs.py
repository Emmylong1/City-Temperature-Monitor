import os
import ipfshttpclient
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# IPFS connection parameters
IPFS_HOST = os.environ.get("IPFS_HOST", "localhost")
IPFS_PORT = os.environ.get("IPFS_PORT", "5001")
IPFS_PROTOCOL = os.environ.get("IPFS_PROTOCOL", "http")

# IPFS API URL
IPFS_API = f"{IPFS_PROTOCOL}://{IPFS_HOST}:{IPFS_PORT}/api/v0"

async def store_on_ipfs(data):
    """Store data on IPFS"""
    try:
        # Connect to IPFS
        with ipfshttpclient.connect(IPFS_API) as client:
            # Add data to IPFS
            result = client.add_str(data)
            logger.info(f"Stored data on IPFS with hash: {result}")
            return result
    except Exception as e:
        logger.error(f"Error storing data on IPFS: {str(e)}")
        # Return a mock hash if IPFS is not available
        import hashlib
        mock_hash = hashlib.md5(data.encode()).hexdigest()
        logger.warning(f"Using mock IPFS hash: {mock_hash}")
        return f"mock-{mock_hash}"

async def retrieve_from_ipfs(hash):
    """Retrieve data from IPFS"""
    try:
        # Connect to IPFS
        with ipfshttpclient.connect(IPFS_API) as client:
            # Get data from IPFS
            data = client.cat(hash).decode('utf-8')
            return data
    except Exception as e:
        logger.error(f"Error retrieving data from IPFS with hash {hash}: {str(e)}")
        raise
