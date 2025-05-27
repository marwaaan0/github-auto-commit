# GitHub Auto Commit - Daily Contribution Automation

Automatically maintain your GitHub contribution activity with meaningful daily commits.

## Features

- 🔄 **Automated Daily Commits**: Creates meaningful commits every day
- 📝 **Dynamic Content**: Updates a daily log file with timestamps and progress notes
- ⚙️ **Configurable**: Customize commit messages, timing, and behavior
- 🚫 **Weekend Control**: Option to skip weekends
- 📊 **Logging**: Comprehensive logging for monitoring and debugging
- ☁️ **Cloud Ready**: Includes GitHub Actions workflow for cloud automation
- 🖥️ **Windows Friendly**: Includes batch files for easy execution

## Quick Start

1. **Setup the environment:**
   ```bash
   python setup.py
   ```

2. **Test with a single commit:**
   ```bash
   python scheduler.py --once
   ```

3. **Start the scheduler:**
   ```bash
   python scheduler.py --schedule
   ```

## Installation

### Prerequisites
- Python 3.7+
- Git installed and configured
- GitHub repository (optional for remote push)

### Setup Steps

1. **Clone or download this repository**
2. **Run the setup script:**
   ```bash
   python setup.py
   ```
   This will:
   - Install required dependencies
   - Configure Git if needed
   - Set up repository settings
   - Create batch files for Windows users

## Configuration

Edit `config.json` to customize behavior:

```json
{
  "repository": {
    "local_path": ".",
    "remote_url": "https://github.com/yourusername/your-repo.git",
    "branch": "main"
  },
  "commit": {
    "message_templates": [
      "Daily update: {date}",
      "Automated commit: {date}",
      "Daily maintenance: {date}"
    ],
    "file_to_update": "daily_log.md",
    "commit_time": "09:00",
    "timezone": "UTC"
  },
  "schedule": {
    "enabled": true,
    "skip_weekends": false,
    "custom_schedule": []
  }
}
```

## Usage

### Command Line Options

```bash
# Run a single commit immediately
python scheduler.py --once

# Start the continuous scheduler
python scheduler.py --schedule

# On Windows, use batch files
start_scheduler.bat    # Start scheduler
run_once.bat          # Single commit
```

### What It Does

1. **Creates/Updates Daily Log**: Updates `daily_log.md` with:
   - Current date and time
   - Progress notes
   - Activity status

2. **Commits Changes**: Creates a commit with a randomized message from your templates

3. **Pushes to Remote**: Automatically pushes to your GitHub repository (if configured)

## GitHub Actions (Cloud Automation)

For fully automated cloud-based commits:

1. **Enable during setup** or manually create `.github/workflows/auto-commit.yml`
2. **Push to GitHub**: The workflow will run daily at 9:00 AM UTC
3. **Manual trigger**: You can also trigger it manually from the Actions tab

## File Structure

```
githubauto/
├── github_auto_commit.py    # Main automation logic
├── scheduler.py             # Scheduling and execution
├── setup.py                 # Initial setup and configuration
├── config.json              # Configuration settings
├── requirements.txt         # Python dependencies
├── daily_log.md            # Generated daily log (created automatically)
├── automation.log          # Log file (created automatically)
├── start_scheduler.bat     # Windows batch file
├── run_once.bat           # Windows batch file
└── .github/workflows/     # GitHub Actions (optional)
    └── auto-commit.yml
```

## Customization

### Commit Messages
Add your own templates to `config.json`:
```json
"message_templates": [
  "Daily progress: {date}",
  "Keeping the streak alive: {date}",
  "Another day, another commit: {date}"
]
```

### Custom Schedule
Skip specific dates:
```json
"custom_schedule": ["2024-12-25", "2024-01-01"]
```

### Different Content
Change the file that gets updated:
```json
"file_to_update": "progress.md"
```

## Troubleshooting

### Common Issues

1. **Git not configured**:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **Permission denied (GitHub)**:
   - Use personal access token instead of password
   - Configure SSH keys for authentication

3. **Scheduler not running**:
   - Check the log file `automation.log`
   - Ensure Python path is correct
   - Verify configuration in `config.json`

### Logs
Check `automation.log` for detailed information about execution and any errors.

## Best Practices

1. **Meaningful Commits**: The tool creates actual content changes, not empty commits
2. **Reasonable Frequency**: Default is once per day to maintain natural activity
3. **Content Variety**: Randomized commit messages and dynamic content
4. **Error Handling**: Comprehensive logging and error recovery

## Security Notes

- Never commit sensitive information
- Use environment variables for tokens in production
- Review generated content before pushing to public repositories

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
