#!/usr/bin/env python3
"""
GitHub Auto Commit - Daily Contribution Automation
Automatically creates meaningful commits to maintain GitHub contribution activity.
"""

import os
import json
import logging
import random
from datetime import datetime, timedelta
from pathlib import Path
import git
from git import Repo, InvalidGitRepositoryError


class GitHubAutoCommit:
    def __init__(self, config_path="config.json"):
        """Initialize the auto commit system."""
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.repo = None
        
    def load_config(self, config_path):
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Config file {config_path} not found")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in config file {config_path}")
            raise
    
    def setup_logging(self):
        """Setup logging configuration."""
        if self.config['logging']['enabled']:
            logging.basicConfig(
                level=getattr(logging, self.config['logging']['level']),
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(self.config['logging']['log_file']),
                    logging.StreamHandler()
                ]
            )
        
    def initialize_repo(self):
        """Initialize or connect to the Git repository."""
        repo_path = self.config['repository']['local_path']
        
        try:
            self.repo = Repo(repo_path)
            logging.info(f"Connected to existing repository at {repo_path}")
        except InvalidGitRepositoryError:
            logging.info(f"Initializing new repository at {repo_path}")
            self.repo = Repo.init(repo_path)
            
        # Set up remote if specified
        remote_url = self.config['repository']['remote_url']
        if remote_url and 'origin' not in [remote.name for remote in self.repo.remotes]:
            self.repo.create_remote('origin', remote_url)
            logging.info(f"Added remote origin: {remote_url}")
    
    def create_daily_content(self):
        """Create or update daily content file."""
        file_path = self.config['commit']['file_to_update']
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Create daily log content
        daily_entry = f"""
## Daily Entry - {current_date}

**Time:** {current_time}
**Status:** Active
**Notes:** Automated daily update to maintain contribution activity.

### Today's Progress
- Maintained consistent development workflow
- Automated contribution tracking active
- Repository health check completed

---
"""
        
        # Read existing content or create new
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            existing_content = "# Daily Development Log\n\nThis file tracks daily development activity.\n\n"
        
        # Prepend new entry to existing content
        updated_content = existing_content.replace(
            "# Daily Development Log\n\nThis file tracks daily development activity.\n\n",
            f"# Daily Development Log\n\nThis file tracks daily development activity.\n\n{daily_entry}"
        )
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        logging.info(f"Updated daily content in {file_path}")
        return file_path
    
    def generate_commit_message(self):
        """Generate a commit message from templates."""
        templates = self.config['commit']['message_templates']
        template = random.choice(templates)
        current_date = datetime.now().strftime("%Y-%m-%d")
        return template.format(date=current_date)
    
    def make_commit(self):
        """Create and push a commit."""
        try:
            # Ensure repository is initialized
            if not self.repo:
                self.initialize_repo()
            
            # Create daily content
            file_path = self.create_daily_content()
            
            # Stage the file
            self.repo.index.add([file_path])
            
            # Check if there are changes to commit
            if not self.repo.index.diff("HEAD"):
                logging.info("No changes to commit")
                return False
            
            # Create commit
            commit_message = self.generate_commit_message()
            commit = self.repo.index.commit(commit_message)
            logging.info(f"Created commit: {commit.hexsha[:8]} - {commit_message}")
            
            # Push to remote if configured
            if 'origin' in [remote.name for remote in self.repo.remotes]:
                try:
                    origin = self.repo.remote('origin')
                    branch = self.config['repository']['branch']
                    origin.push(branch)
                    logging.info(f"Pushed to remote origin/{branch}")
                except Exception as e:
                    logging.warning(f"Failed to push to remote: {e}")
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to make commit: {e}")
            return False
    
    def should_commit_today(self):
        """Check if a commit should be made today based on configuration."""
        if not self.config['schedule']['enabled']:
            return False
        
        today = datetime.now()
        
        # Check if weekends should be skipped
        if self.config['schedule']['skip_weekends'] and today.weekday() >= 5:
            logging.info("Skipping commit - weekend")
            return False
        
        # Check custom schedule (if any)
        custom_schedule = self.config['schedule'].get('custom_schedule', [])
        if custom_schedule:
            today_str = today.strftime("%Y-%m-%d")
            if today_str in custom_schedule:
                logging.info("Skipping commit - custom schedule")
                return False
        
        return True
    
    def run(self):
        """Main execution method."""
        logging.info("Starting GitHub Auto Commit")
        
        if not self.should_commit_today():
            return False
        
        success = self.make_commit()
        
        if success:
            logging.info("Daily commit completed successfully")
        else:
            logging.error("Daily commit failed")
        
        return success


if __name__ == "__main__":
    auto_commit = GitHubAutoCommit()
    auto_commit.run()
