#!/usr/bin/env python3
"""
================================================================================
PROBLEM STATEMENT 2: System Monitoring Scripts
================================================================================
Application Health Checker Script

Checks application uptime and HTTP status codes.
Determines if application is 'up' or 'down'.

Features:
  - HTTP endpoint availability checking
  - HTTP status code validation
  - Retry logic (3 attempts with 2-second delays)
  - Timeout: 5 seconds default
  - JSON output for integration
  - Detailed error handling
  - File and console logging
  - Exit codes for automation (0: healthy, 1: issues detected)
================================================================================
"""

import requests
import logging
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import time

# Configuration
DEFAULT_TIMEOUT = 5  # seconds
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds

# Setup logging
LOG_DIR = Path.home() / ".app_health_checker"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app_health.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ApplicationHealthChecker:
    """Check application health by monitoring HTTP endpoints."""
    
    def __init__(self, endpoints: List[Dict], timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize the health checker.
        
        Args:
            endpoints: List of dicts with 'url' and optional 'expected_status'
            timeout: Request timeout in seconds
        """
        self.endpoints = endpoints
        self.timeout = timeout
        self.results = []
    
    def check_endpoint(self, url: str, expected_status: int = 200) -> Tuple[bool, int, str]:
        """
        Check a single endpoint with retries.
        
        Args:
            url: The endpoint URL to check
            expected_status: Expected HTTP status code
            
        Returns:
            Tuple of (is_healthy, status_code, message)
        """
        for attempt in range(RETRY_ATTEMPTS):
            try:
                logger.info(f"Checking {url} (attempt {attempt + 1}/{RETRY_ATTEMPTS})")
                response = requests.get(url, timeout=self.timeout, verify=False)
                status_code = response.status_code
                
                is_healthy = status_code == expected_status
                
                if is_healthy:
                    logger.info(f"✅ {url} is UP (Status: {status_code})")
                    return True, status_code, f"Application is UP"
                else:
                    logger.warning(f"⚠️  {url} returned unexpected status: {status_code}")
                    if attempt < RETRY_ATTEMPTS - 1:
                        time.sleep(RETRY_DELAY)
                        continue
                    return False, status_code, f"Unexpected status code: {status_code}"
                    
            except requests.exceptions.Timeout:
                logger.warning(f"⏱️  Timeout connecting to {url}")
                if attempt < RETRY_ATTEMPTS - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                return False, 0, "Connection timeout"
                
            except requests.exceptions.ConnectionError:
                logger.warning(f"❌ Connection error to {url}")
                if attempt < RETRY_ATTEMPTS - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                return False, 0, "Connection refused"
                
            except Exception as e:
                logger.error(f"Error checking {url}: {e}")
                if attempt < RETRY_ATTEMPTS - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                return False, 0, f"Error: {str(e)}"
        
        return False, 0, "Failed after all retries"
    
    def check_all_endpoints(self) -> Dict:
        """Check all configured endpoints."""
        logger.info("=" * 70)
        logger.info(f"Application Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'endpoints': [],
            'overall_status': 'UP',
            'healthy_count': 0,
            'unhealthy_count': 0
        }
        
        for endpoint in self.endpoints:
            url = endpoint.get('url')
            expected_status = endpoint.get('expected_status', 200)
            
            if not url:
                logger.warning("Skipping endpoint without URL")
                continue
            
            is_healthy, status_code, message = self.check_endpoint(url, expected_status)
            
            endpoint_result = {
                'url': url,
                'status': 'UP' if is_healthy else 'DOWN',
                'http_status': status_code,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
            results['endpoints'].append(endpoint_result)
            
            if is_healthy:
                results['healthy_count'] += 1
            else:
                results['unhealthy_count'] += 1
                results['overall_status'] = 'DOWN'
        
        return results
    
    def print_report(self, results: Dict):
        """Print a formatted health report."""
        logger.info("\n--- Health Check Results ---")
        
        for endpoint in results['endpoints']:
            status_icon = "✅" if endpoint['status'] == 'UP' else "❌"
            logger.info(f"{status_icon} {endpoint['url']}")
            logger.info(f"   Status: {endpoint['status']} | HTTP: {endpoint['http_status']}")
            logger.info(f"   Message: {endpoint['message']}")
        
        logger.info("\n--- Summary ---")
        logger.info(f"Overall Status: {results['overall_status']}")
        logger.info(f"Healthy Endpoints: {results['healthy_count']}/{len(results['endpoints'])}")
        logger.info(f"Unhealthy Endpoints: {results['unhealthy_count']}/{len(results['endpoints'])}")
        logger.info("=" * 70 + "\n")
        
        return results['overall_status'] == 'UP'


def main():
    """Main function to run health checks."""
    # Example endpoints to check
    endpoints = [
        {'url': 'http://localhost:8080', 'expected_status': 200},
        {'url': 'http://localhost:4499', 'expected_status': 200},  # Wisecow app
        {'url': 'https://www.google.com', 'expected_status': 200},
    ]
    
    # You can also pass endpoints via command line or config file
    if len(sys.argv) > 1:
        try:
            endpoints = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            logger.error("Invalid JSON format for endpoints")
            sys.exit(1)
    
    checker = ApplicationHealthChecker(endpoints)
    results = checker.check_all_endpoints()
    is_healthy = checker.print_report(results)
    
    # Save results to JSON file
    results_file = LOG_DIR / "latest_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"Results saved to {results_file}")
    
    sys.exit(0 if is_healthy else 1)


if __name__ == "__main__":
    main()

