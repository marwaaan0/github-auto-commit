#!/usr/bin/env python3
"""
Setup script for GitHub Auto Commit
Handles initial configuration and dependency installation.
"""

import os
import json
import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install required Python packages."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False


def setup_git_config():
    """Setup basic Git configuration if not already configured."""
    try:
        # Check if git user is configured
        result = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
        if not result.stdout.strip():
            name = input("Enter your Git username: ")
            subprocess.run(["git", "config", "user.name", name])
        
        result = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
        if not result.stdout.strip():
            email = input("Enter your Git email: ")
            subprocess.run(["git", "config", "user.email", email])
        
        print("✓ Git configuration verified")
        return True
    except Exception as e:
        print(f"✗ Git configuration failed: {e}")
        return False


def configure_repository():
    """Configure repository settings."""
    config_path = "config.json"
    
    # Load existing config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("\n=== Repository Configuration ===")
    
    # Get repository URL
    current_remote = config['repository']['remote_url']
    if not current_remote:
        remote_url = input("Enter your GitHub repository URL (optional, press Enter to skip): ").strip()
        if remote_url:
            config['repository']['remote_url'] = remote_url
    
    # Get branch name
    current_branch = config['repository']['branch']
    branch = input(f"Enter branch name (current: {current_branch}): ").strip()
    if branch:
        config['repository']['branch'] = branch
    
    # Get commit time
    current_time = config['commit']['commit_time']
    commit_time = input(f"Enter daily commit time in HH:MM format (current: {current_time}): ").strip()
    if commit_time:
        config['commit']['commit_time'] = commit_time
    
    # Weekend commits
    skip_weekends = config['schedule']['skip_weekends']
    weekend_choice = input(f"Skip weekend commits? (current: {skip_weekends}) [y/n]: ").strip().lower()
    if weekend_choice in ['y', 'yes']:
        config['schedule']['skip_weekends'] = True
    elif weekend_choice in ['n', 'no']:
        config['schedule']['skip_weekends'] = False
    
    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✓ Configuration updated")
    return True


def create_batch_files():
    """Create Windows batch files for easy execution."""
    
    # Start scheduler batch file
    start_batch = """@echo off
echo Starting GitHub Auto Commit Scheduler...
python scheduler.py --schedule
pause
"""
    
    with open("start_scheduler.bat", "w") as f:
        f.write(start_batch)
    
    # Run once batch file
    once_batch = """@echo off
echo Running single commit...
python scheduler.py --once
pause
"""
    
    with open("run_once.bat", "w") as f:
        f.write(once_batch)
    
    print("✓ Batch files created (start_scheduler.bat, run_once.bat)")


def create_github_action():
    """Create GitHub Action workflow for cloud automation."""
    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: Daily Auto Commit

on:
  schedule:
    # Run daily at 9:00 AM UTC
    - cron: '0 9 * * *'
  workflow_dispatch: # Allow manual trigger

jobs:
  auto-commit:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Configure Git
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
    
    - name: Run auto commit
      run: python scheduler.py --once
    
    - name: Push changes
      run: |
        git push
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""
    
    workflow_path = workflow_dir / "auto-commit.yml"
    with open(workflow_path, "w") as f:
        f.write(workflow_content)
    
    print("✓ GitHub Action workflow created (.github/workflows/auto-commit.yml)")


def main():
    """Main setup function."""
    print("=== GitHub Auto Commit Setup ===\n")
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup Git
    if not setup_git_config():
        return False
    
    # Configure repository
    if not configure_repository():
        return False
    
    # Create batch files for Windows
    create_batch_files()
    
    # Ask about GitHub Actions
    github_action = input("\nCreate GitHub Action for cloud automation? [y/n]: ").strip().lower()
    if github_action in ['y', 'yes']:
        create_github_action()
    
    print("\n=== Setup Complete! ===")
    print("\nNext steps:")
    print("1. Run 'python scheduler.py --once' to test a single commit")
    print("2. Run 'python scheduler.py --schedule' to start the scheduler")
    print("3. On Windows, you can use 'start_scheduler.bat' or 'run_once.bat'")
    print("4. If you created GitHub Actions, push this repository to GitHub")
    
    return True


if __name__ == "__main__":
    main()
