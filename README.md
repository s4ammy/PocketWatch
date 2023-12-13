# PocketWatch
Sends a discord webhook when it detects a new transaction with less than 6 confirmations

## Requirements
- Python
- discord-webhook (pip install discord-webhook)
- schedule (pip install schedule)
- requests (pip install requests)

## Configuring `crypto_config.py`
- CRYPTO_ADDRESS - add your crypto addresses here
- WEBHOOK_URL - add your discord webhook url here
- SCAN_DELAY - how often to check for new transactions (in seconds)