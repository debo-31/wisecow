#!/usr/bin/env python3
"""
================================================================================
PROBLEM STATEMENT 2: System Monitoring Scripts
================================================================================
System Health Monitoring Script

Monitors CPU, memory, disk space, and running processes.
Sends alerts when metrics exceed predefined thresholds.

Features:
  - CPU usage monitoring (threshold: 80%)
  - Memory usage monitoring (threshold: 80%)
  - Disk space monitoring (threshold: 80%)
  - Running processes monitoring (threshold: 100)
  - Top 5 processes by CPU and memory
  - File and console logging
  - Exit codes for automation (0: healthy, 1: issues detected)
================================================================================
"""

import psutil
import logging
import sys
from datetime import datetime
from pathlib import Path

# Configuration
CPU_THRESHOLD = 80  # percentage
MEMORY_THRESHOLD = 80  # percentage
DISK_THRESHOLD = 80  # percentage
PROCESS_THRESHOLD = 100  # number of processes

# Setup logging
LOG_DIR = Path.home() / ".system_monitor"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "system_health.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def check_cpu_usage():
    """Check CPU usage and alert if threshold exceeded."""
    cpu_percent = psutil.cpu_percent(interval=1)
    logger.info(f"CPU Usage: {cpu_percent}%")
    
    if cpu_percent > CPU_THRESHOLD:
        logger.warning(f"⚠️  ALERT: CPU usage is {cpu_percent}% (threshold: {CPU_THRESHOLD}%)")
        return False
    return True


def check_memory_usage():
    """Check memory usage and alert if threshold exceeded."""
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    logger.info(f"Memory Usage: {memory_percent}% ({memory.used / (1024**3):.2f}GB / {memory.total / (1024**3):.2f}GB)")
    
    if memory_percent > MEMORY_THRESHOLD:
        logger.warning(f"⚠️  ALERT: Memory usage is {memory_percent}% (threshold: {MEMORY_THRESHOLD}%)")
        return False
    return True


def check_disk_usage():
    """Check disk usage and alert if threshold exceeded."""
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    logger.info(f"Disk Usage: {disk_percent}% ({disk.used / (1024**3):.2f}GB / {disk.total / (1024**3):.2f}GB)")
    
    if disk_percent > DISK_THRESHOLD:
        logger.warning(f"⚠️  ALERT: Disk usage is {disk_percent}% (threshold: {DISK_THRESHOLD}%)")
        return False
    return True


def check_running_processes():
    """Check number of running processes and alert if threshold exceeded."""
    process_count = len(psutil.pids())
    logger.info(f"Running Processes: {process_count}")
    
    if process_count > PROCESS_THRESHOLD:
        logger.warning(f"⚠️  ALERT: Number of processes is {process_count} (threshold: {PROCESS_THRESHOLD})")
        return False
    return True


def get_top_processes():
    """Get top 5 processes by CPU and memory usage."""
    logger.info("\n--- Top 5 Processes by CPU Usage ---")
    try:
        processes = sorted(
            [p for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])
             if p.info['cpu_percent'] is not None],
            key=lambda p: p.info['cpu_percent'], reverse=True)[:5]
        for proc in processes:
            logger.info(f"  {proc.info['name']}: {proc.info['cpu_percent']}%")
    except Exception as e:
        logger.warning(f"Could not retrieve CPU process info: {e}")

    logger.info("\n--- Top 5 Processes by Memory Usage ---")
    try:
        processes = sorted(
            [p for p in psutil.process_iter(['pid', 'name', 'memory_percent'])
             if p.info['memory_percent'] is not None],
            key=lambda p: p.info['memory_percent'], reverse=True)[:5]
        for proc in processes:
            logger.info(f"  {proc.info['name']}: {proc.info['memory_percent']}%")
    except Exception as e:
        logger.warning(f"Could not retrieve memory process info: {e}")


def generate_report():
    """Generate a comprehensive system health report."""
    logger.info("=" * 60)
    logger.info(f"System Health Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    results = {
        'cpu': check_cpu_usage(),
        'memory': check_memory_usage(),
        'disk': check_disk_usage(),
        'processes': check_running_processes()
    }
    
    get_top_processes()
    
    logger.info("=" * 60)
    
    # Summary
    all_ok = all(results.values())
    if all_ok:
        logger.info("✅ All systems healthy!")
    else:
        failed = [k for k, v in results.items() if not v]
        logger.warning(f"❌ Issues detected in: {', '.join(failed)}")
    
    logger.info("=" * 60 + "\n")
    
    return all_ok


if __name__ == "__main__":
    try:
        success = generate_report()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Error during health check: {e}", exc_info=True)
        sys.exit(1)

