import requests
import schedule
import time

from discord_webhook import DiscordWebhook, DiscordEmbed

from crypto_config import CRYPTO_ADDRESS, WEBHOOK_URL, SCAN_DELAY

LOW_CONF_TRANSACTIONS = []

def get_data_from_site(api_url):
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data

        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def find_low_confirmations_tx(json_data):
    try:
        transactions = json_data.get("txs", [])

        low_conf_txs = [tx for tx in transactions if tx.get("confirmations", 0) < 6]#6 max confirmations seems standard

        return low_conf_txs

    except Exception as e:
        print(f"An error occurred while finding low confirmations transactions: {str(e)}")

def send_webhook(crypto, hash, confirmations):
    webhook = DiscordWebhook(url=WEBHOOK_URL, username=f"{crypto.upper()} Transaction Detector")

    embed = DiscordEmbed(title="New transaction detected", description=f"Hash: {hash}\nConfirmations: {confirmations}", color="a882ff")

    embed.set_author(
        name=crypto.upper(),
        url=f"https://live.blockcypher.com/{crypto}/tx/{hash}",
        icon_url="https://www.iconarchive.com/download/i109520/cjdowner/cryptocurrency-flat/Dollar-USD.1024.png"
    )

    embed.add_embed_field(name='', value=f"[View on blockchain](https://live.blockcypher.com/{crypto}/tx/{hash})")

    webhook.add_embed(embed)
    response = webhook.execute()

def scan_crypto_transactions(crypto):
    api_url = f"https://api.blockcypher.com/v1/{crypto}/main/addrs/{CRYPTO_ADDRESS[crypto]}/full?limit=10"
    json_data = get_data_from_site(api_url)

    if json_data:
        low_confirmations_txs = find_low_confirmations_tx(json_data)

        if low_confirmations_txs:
            for tx in low_confirmations_txs:
                tx_hash = tx["hash"]

                if tx_hash not in LOW_CONF_TRANSACTIONS:
                    send_webhook(crypto, tx_hash, tx["confirmations"])

                    LOW_CONF_TRANSACTIONS.append(tx_hash)

def job():
    print("Checking for new transactions...")
    for crypto in CRYPTO_ADDRESS.keys():
        scan_crypto_transactions(crypto)
    
    print("Waiting 5 minutes...")

job()

schedule.every(SCAN_DELAY).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)