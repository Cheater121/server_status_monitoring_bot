# Server Status Bot

This Telegram bot periodically checks the status of a server and notifies a group chat about any issues. It also performs a daily check at a specified time to report the number of days without server issues.

## Features

- Sends requests to a server URL every minute.
- Notifies a group chat if the server is not responding.
- Performs a daily check at a specified time to report the number of days without server issues.
- Controlled by allowed users specified by user IDs.
- Uses SQLite database to store server events.
- Start the bot to begin monitoring the server.
- Stop the bot to halt monitoring.

## Installation

1. Clone this repository:
```
git clone git@github.com:Cheater121/server_status_monitoring_bot.git
```
2. Install virtual environment to your working directory with command:
```
python3 -m venv venv
```
3. Activate your venv. For Linux use:
```
source venv/bin/activate
```
4. Install the required dependencies:
```
pip install -r requirements.txt
```
5. Rename `.env.example` to `.env` and update it with your data (telegram bot api token etc.).
6. Run bot with command:
```
python3 main.py
```

## Usage

Add bot to your Telegram Group and write `/start` in chat. The bot will start monitoring the server and send notifications to the configured group chat about server events.

To stop the bot, send the `/stop` command to the bot in the Telegram chat. 

## Additionally setup information

You can create Linux systemd service. To make this you need to create `your_bot_name.service` in `/etc/systemd/system/` directory:
```
[Unit]
Description=Server Status Monitoring Bot
After=network.target

[Service]
User=your_user
WorkingDirectory=/home/your_user/path/to/server_status_monitoring_bot
Environment="PATH=/home/your_user/path/to/server_status_monitoring_bot/venv/bin:$PATH"
ExecStart=/home/your_user/path/to/server_status_monitoring_bot/venv/bin/python main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
Fill it with your actual data and enjoy. 
