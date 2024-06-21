import requests
from logzero import logger
from datetime import datetime

from models.bitcoin_transaction import BitcoinTransaction
from utils.mongo import get_one_from_mongo, save_to_mongo

# URL to use API for transactions from blockcypher
BASE_URL = 'https://api.blockcypher.com/v1/btc/main/txs/'


# get transaction_hash and return details about the transaction
# also cache the details into mongo (before using blockcypher we also validate if it is not already in cache)
def get_transaction_info(transaction_hash) -> BitcoinTransaction | None:
    url = f'{BASE_URL}{transaction_hash}'

    try:
        # is in cache
        data = get_one_from_mongo(collection_name="transactions", query={'hash': transaction_hash})
        if not data:
            # not in cache (mongodb) so we use blockcypher api
            response = requests.get(url)
            if response.status_code == 404:
                logger.error(f"Transaction not found: {transaction_hash}")
                return None
            response.raise_for_status()  # Raise an error for other bad status codes

            data = response.json()

            # Transform the data to match the expected response format
            transformed_data = {
                "hash": data.get("hash"),
                "fee": data.get("fees"),
                "inputs": [{
                    "address": inp["addresses"][0] if "addresses" in inp and isinstance(inp["addresses"], list) else inp.get("address", "Unknown"),
                    "value": inp.get("output_value", 0)
                } for inp in data.get("inputs", [])],
                "outputs": [{
                    "address": out["addresses"][0] if "addresses" in out and isinstance(out["addresses"], list) else out.get("address", "Unknown"),
                    "value": out.get("value", 0)
                } for out in data.get("outputs", [])],
                "transaction_index": data.get("tx_index", 0),
                "block_time": int(datetime.strptime(data.get("confirmed"), "%Y-%m-%dT%H:%M:%SZ").timestamp()) if data.get("confirmed") else 0
            }

            # Save to MongoDB (cache the transaction information)
            save_to_mongo(transformed_data, collection_name="transactions")
            bitcoin_transaction: BitcoinTransaction = BitcoinTransaction(**transformed_data)
        else:
            bitcoin_transaction = data

        return bitcoin_transaction
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching transaction data: {e}")
        return None
    except Exception as e:
        logger.error(f"Unknown error:: {e}")
        raise
