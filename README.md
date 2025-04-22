# MTG Article Discord Bot

This bot monitors the Magic: The Gathering news archive and sends notifications to a Discord channel when new articles are published.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a Discord webhook:
   - Go to your Discord server
   - Right-click on the channel where you want to receive notifications
   - Select "Edit Channel"
   - Go to "Integrations"
   - Click "Create Webhook"
   - Copy the webhook URL

3. Configure the bot:
   - Copy `.env.example` to `.env`
   - Replace `your_webhook_url_here` with your actual Discord webhook URL

## Usage

Run the bot with:
```bash
python mtg_article_bot.py
```

The bot will:
- Check for new articles every 5 minutes
- Send a notification to your Discord channel when a new article is found
- Store the last seen article to avoid duplicate notifications

## Features

- Monitors the Magic: The Gathering news archive
- Sends formatted Discord embeds with article titles and links
- Prevents duplicate notifications
- Error handling and logging
- Configurable check interval 