"""
pretty_logger.py - Beautified console logging with emoji support for Python

Usage:
    from pretty_logger import logger
    
    logger.info("User logged in")
    logger.warn("Session expiring soon")
    logger.error("Failed to connect to database")
    logger.success("Operation completed successfully")
    logger.debug("Variable state:", {"foo": "bar"})
"""

import json
import logging
import os
import sys
import datetime
from typing import Any, Dict, List, Optional, Union

try:
    # Try to import colorama for Windows color support
    from colorama import init as colorama_init
    colorama_init()
except ImportError:
    print("⚠️  For better color support on Windows, install colorama:")
    print("pip install colorama")

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLACK = "\033[40m"


class PrettyLogger:
    def __init__(self, name: str = "app"):
        self.name = name
        self.debug_enabled = os.environ.get("DEBUG", "false").lower() in ["true", "1", "yes"]
        
    def _format_object(self, obj: Any) -> str:
        """Format objects for better readability"""
        if isinstance(obj, (dict, list)):
            return json.dumps(obj, indent=2, default=str)
        return str(obj)
    
    def _timestamp(self) -> str:
        """Generate a formatted timestamp"""
        now = datetime.datetime.now()
        return f"{Colors.DIM}[{now.isoformat(timespec='milliseconds')}]{Colors.RESET}"
    
    def _format_message(self, *args) -> str:
        """Format all arguments into a single message string"""
        message_parts = []
        for arg in args:
            if isinstance(arg, (dict, list)):
                message_parts.append(self._format_object(arg))
            else:
                message_parts.append(str(arg))
        return " ".join(message_parts)
    
    def info(self, *args):
        """Log an info message"""
        message = self._format_message(*args)
        print(f"{self._timestamp()} {Colors.BLUE}ℹ️  INFO{Colors.RESET}    {message}")
    
    def warn(self, *args):
        """Log a warning message"""
        message = self._format_message(*args)
        print(f"{self._timestamp()} {Colors.YELLOW}⚠️  WARNING{Colors.RESET} {message}")
    
    def error(self, *args):
        """Log an error message"""
        message = self._format_message(*args)
        print(f"{self._timestamp()} {Colors.RED}🔴 ERROR{Colors.RESET}   {message}")
    
    def success(self, *args):
        """Log a success message"""
        message = self._format_message(*args)
        print(f"{self._timestamp()} {Colors.GREEN}✅ SUCCESS{Colors.RESET} {message}")
    
    def debug(self, *args):
        """Log a debug message (only if DEBUG environment variable is set)"""
        if not self.debug_enabled:
            return
        
        message = self._format_message(*args)
        print(f"{self._timestamp()} {Colors.MAGENTA}🔍 DEBUG{Colors.RESET}   {message}")
    
    def divider(self, title: str = ""):
        """Create a visual divider with optional title"""
        width = os.get_terminal_size().columns if sys.stdout.isatty() else 80
        
        if title:
            line = "─" * (width - len(title) - 4)
            print(f"{Colors.DIM}┌─ {Colors.BOLD}{title}{Colors.RESET}{Colors.DIM} {line}{Colors.RESET}")
        else:
            line = "─" * (width - 2)
            print(f"{Colors.DIM}┌{line}┐{Colors.RESET}")
    
    def divider_end(self):
        """End a divider section"""
        width = os.get_terminal_size().columns if sys.stdout.isatty() else 80
        line = "─" * (width - 2)
        print(f"{Colors.DIM}└{line}┘{Colors.RESET}")


# Create a singleton instance for import
logger = PrettyLogger()

if __name__ == "__main__":
    # Run a demo if this file is executed directly
    logger.divider("💫 PYTHON LOGGER DEMO")
    logger.info("Starting application...")
    logger.debug("Config loaded", {
        "environment": "development",
        "features": {
            "auth": True,
            "analytics": False,
            "dark_mode": True
        },
        "version": "1.0.0"
    })
    logger.success("Connected to database")
    logger.warn("Cache miss for user profile")
    logger.error("Payment processing failed", {
        "error": "Failed to process payment",
        "timestamp": datetime.datetime.now().isoformat()
    })
    logger.info("Processing complete")
    logger.divider_end() 