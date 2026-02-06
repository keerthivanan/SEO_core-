"""
Enterprise logging system for RankForge AI
Structured JSON logging with request tracking
"""

import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime
import uuid
from contextvars import ContextVar

# Context variable for request ID tracking
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Enterprise-grade JSON formatter with request tracking
    """
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        # Add request_id if available
        request_id = request_id_ctx.get()
        if request_id:
            log_record['request_id'] = request_id
        
        # Add timestamp
        log_record['timestamp'] = datetime.utcnow().isoformat()
        
        # Add service info
        log_record['service'] = 'rankforge-api'
        log_record['level'] = record.levelname

def setup_logging():
    """
    Configure enterprise logging system
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: str):
    """Get logger for specific module"""
    return logging.getLogger(name)

def set_request_id(request_id: str = None):
    """Set request ID for current context"""
    if not request_id:
        request_id = str(uuid.uuid4())
    request_id_ctx.set(request_id)
    return request_id
