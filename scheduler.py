#!/usr/bin/env python3
"""
Scheduler for GitHub Auto Commit
Handles timing and automated execution of daily commits.
"""

import schedule
import time
import logging
import json
from datetime import datetime
from github_auto_commit import GitHubAutoCommit


class CommitScheduler:
    def __init__(self, config_path="config.json"):
        """Initialize the scheduler."""
        self.config_path = config_path
        self.auto_commit = GitHubAutoCommit(config_path)
        self.load_schedule_config()
        
    def load_schedule_config(self):
        """Load scheduling configuration."""
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        self.commit_time = config['commit']['commit_time']
        self.enabled = config['schedule']['enabled']
        
    def scheduled_commit(self):
        """Execute scheduled commit."""
        logging.info(f"Executing scheduled commit at {datetime.now()}")
        try:
            success = self.auto_commit.run()
            if success:
                logging.info("Scheduled commit completed successfully")
            else:
                logging.warning("Scheduled commit completed with issues")
        except Exception as e:
            logging.error(f"Scheduled commit failed: {e}")
    
    def setup_schedule(self):
        """Setup the daily schedule."""
        if not self.enabled:
            logging.info("Scheduling is disabled")
            return
        
        # Schedule daily commit
        schedule.every().day.at(self.commit_time).do(self.scheduled_commit)
        logging.info(f"Scheduled daily commit at {self.commit_time}")
        
        # Optional: Add some randomization to avoid detection
        # schedule.every().day.at("09:00").do(self.scheduled_commit)
        # schedule.every().day.at("14:30").do(self.scheduled_commit)
        # schedule.every().day.at("18:45").do(self.scheduled_commit)
    
    def run_scheduler(self):
        """Run the scheduler continuously."""
        self.setup_schedule()
        
        logging.info("Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user")
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
    
    def run_once(self):
        """Run a single commit immediately."""
        logging.info("Running immediate commit")
        return self.auto_commit.run()


def main():
    """Main function with command line options."""
    import sys
    
    scheduler = CommitScheduler()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--once":
            # Run once immediately
            scheduler.run_once()
        elif sys.argv[1] == "--schedule":
            # Run scheduler
            scheduler.run_scheduler()
        else:
            print("Usage: python scheduler.py [--once|--schedule]")
            print("  --once     : Run a single commit immediately")
            print("  --schedule : Start the scheduler for continuous operation")
    else:
        # Default: run scheduler
        scheduler.run_scheduler()


if __name__ == "__main__":
    main()
