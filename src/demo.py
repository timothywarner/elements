"""
demo.py - Demonstration of pretty_logger

Run with:
    python src/demo.py
"""

import asyncio
import random
import time
from pretty_logger import logger

async def simulate_api_call(name, min_time=0.3, max_time=1.2):
    """Simulate an API call with random delay"""
    delay = random.uniform(min_time, max_time)
    logger.debug(f"Starting {name} API call", {"expected_delay": f"{delay:.2f}s"})
    await asyncio.sleep(delay)
    return {"status": "success", "data": f"{name} response", "took": f"{delay:.2f}s"}

async def process_user_data():
    """Process user data with beautiful logging"""
    user_id = f"user_{random.randint(1000, 9999)}"
    
    logger.info(f"Processing data for {user_id}")
    
    # Simulate user authentication
    auth_result = await simulate_api_call("authentication")
    if auth_result["status"] == "success":
        logger.success(f"User {user_id} authenticated", auth_result)
    
    # Simulate profile loading
    try:
        if random.random() < 0.3:  # 30% chance of failure
            raise Exception("Profile not found in database")
        
        profile = await simulate_api_call("profile")
        logger.info(f"Loaded profile for {user_id}", profile)
    except Exception as e:
        logger.error(f"Failed to load profile for {user_id}", {"error": str(e)})
    
    # Simulate permissions check
    permissions = await simulate_api_call("permissions")
    access_level = random.choice(["admin", "user", "guest"])
    logger.info(f"User {user_id} has {access_level} permissions")
    
    if access_level == "guest":
        logger.warn(f"Limited access for {user_id}", {
            "reason": "Guest account has restricted permissions",
            "upgradePath": "/upgrade-account"
        })
    
    # Simulate completing the process
    logger.success(f"Completed processing for {user_id}")

async def main():
    """Main demo function"""
    # Enable debug for this demo
    import os
    os.environ["DEBUG"] = "true"
    
    logger.divider("🔮 PYTHON ASYNC LOGGER DEMO")
    
    logger.info("Starting application...")
    
    # Show some debug data
    logger.debug("Environment", {
        "python_version": "3.9.5",
        "environment": "development",
        "debug_mode": True,
        "log_level": "debug"
    })
    
    # Process multiple users concurrently
    tasks = []
    for _ in range(3):
        tasks.append(asyncio.create_task(process_user_data()))
    
    await asyncio.gather(*tasks)
    
    logger.info("All processing complete")
    logger.divider_end()

if __name__ == "__main__":
    asyncio.run(main()) 