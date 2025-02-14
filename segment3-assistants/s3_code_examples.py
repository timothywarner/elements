"""
TechCorp Cloud API Code Examples
===============================
This file contains practical examples of common API operations using our Python SDK.
"""

import os
from techcorp_cloud import Client, exceptions
from typing import Dict, List, Optional
import logging
import json
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudAPIExamples:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the client with API key."""
        self.api_key = api_key or os.environ.get('TECHCORP_API_KEY')
        self.client = Client(api_key=self.api_key)

    def create_compute_resource(self, name: str, size: str = "medium") -> Dict:
        """
        Example 1: Creating a compute resource with error handling
        """
        try:
            resource = self.client.resources.create(
                name=name,
                type="compute",
                size=size,
                region="us-west"
            )
            logger.info(f"Resource created: {resource['resource_id']}")
            return resource
        except exceptions.RateLimitError:
            logger.error("Rate limit exceeded. Implementing backoff...")
            time.sleep(5)
            return self.create_compute_resource(name, size)
        except exceptions.APIError as e:
            logger.error(f"API error: {str(e)}")
            raise

    def batch_resource_creation(self, resources: List[Dict]) -> List[Dict]:
        """
        Example 2: Batch operation for creating multiple resources
        """
        results = []
        for resource in resources:
            try:
                result = self.client.resources.create(**resource)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to create resource {resource.get('name')}: {str(e)}")
                results.append({"error": str(e), "resource": resource})
        return results

    def run_analysis_with_retry(self, dataset_id: str, max_retries: int = 3) -> Dict:
        """
        Example 3: Running an analysis job with retry logic
        """
        retry_count = 0
        while retry_count < max_retries:
            try:
                job = self.client.analytics.create_job(
                    dataset_id=dataset_id,
                    analysis_type="prediction",
                    parameters={
                        "model": "random_forest",
                        "features": ["price", "quantity", "category"]
                    }
                )
                return self.wait_for_job_completion(job['job_id'])
            except exceptions.APIError as e:
                retry_count += 1
                if retry_count == max_retries:
                    raise
                time.sleep(2 ** retry_count)  # Exponential backoff

    def wait_for_job_completion(self, job_id: str, timeout: int = 300) -> Dict:
        """
        Example 4: Polling for job completion with timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            job_status = self.client.analytics.get_job(job_id)
            if job_status['status'] in ['completed', 'failed']:
                return job_status
            time.sleep(5)
        raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")

    def setup_webhook(self, endpoint_url: str, events: List[str]) -> Dict:
        """
        Example 5: Setting up webhooks for event notifications
        """
        import secrets
        webhook_secret = secrets.token_hex(32)
        
        webhook = self.client.webhooks.create(
            url=endpoint_url,
            events=events,
            secret=webhook_secret
        )
        
        # Store the webhook secret securely
        self._save_webhook_secret(webhook['id'], webhook_secret)
        return webhook

    def _save_webhook_secret(self, webhook_id: str, secret: str) -> None:
        """Securely save webhook secret (implementation depends on your security requirements)"""
        # This is a placeholder - implement secure storage as needed
        pass

def main():
    """Example usage of the API wrapper"""
    # Initialize with your API key
    api = CloudAPIExamples(api_key="your_api_key_here")

    # Example 1: Create a single resource
    resource = api.create_compute_resource("test-server")

    # Example 2: Batch create resources
    resources_to_create = [
        {"name": "server-1", "type": "compute", "size": "small"},
        {"name": "server-2", "type": "compute", "size": "medium"}
    ]
    batch_results = api.batch_resource_creation(resources_to_create)

    # Example 3: Run analysis
    analysis_result = api.run_analysis_with_retry("sample-dataset-123")

    # Example 4: Setup webhook
    webhook = api.setup_webhook(
        "https://your-server.com/webhook",
        ["resource.created", "job.completed"]
    )

if __name__ == "__main__":
    main() 