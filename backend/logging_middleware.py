import logging
import time
import os
from pathlib import Path

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Ensure logs directory exists
logsDir = Path("../logs")
logsDir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s',
  handlers=[
    # File handler only (removed console handler)
    logging.FileHandler(logsDir / "serverlog.txt")
  ]
)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    startTime = time.time()

    # Extract request details
    method = request.method
    path = request.url.path

    # Log the incoming request
    logger.info(f"Request: {method} {path}")

    try:
      # Process the request
      response = await call_next(request)

      # Calculate processing time
      processingTime = time.time() - startTime

      # Log successful response
      logger.info(f"Response: {method} {path} - Status: {response.status_code} - Time: {processingTime:.4f}s")

      return response
    except Exception as e:
      # Calculate processing time
      processingTime = time.time() - startTime

      # Log error
      logger.error(f"Error: {method} {path} - {str(e)} - Time: {processingTime:.4f}s")
      raise

