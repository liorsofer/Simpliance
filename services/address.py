import requests
from logzero import logger

from models.bitcoin_address import BitcoinAddress
from utils.mongo import save_to_mongo, get_one_from_mongo

BASE_URL = 'https://api.blockcypher.com/v1/btc/main/addrs/'


def get_bitcoin_address_info(address) -> BitcoinAddress | None:
    url = f'{BASE_URL}{address}'

    try:
        data = get_one_from_mongo(collection_name="address_info", query={'address': address})
        if not data:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes

            data = response.json()

            # Add the address to the data for reference
            data['address'] = address
            balance = data.get('balance', 0)
            transaction_count = data.get('n_tx', 0)

            address_dict = {
                'address': address,
                'balance': balance,
                'transaction_count': transaction_count
            }

            # Save to MongoDB
            save_to_mongo(address_dict, collection_name="address_info")

        else:
            balance = data.get('balance', 0)
            transaction_count = data.get('transaction_count', 0)

            address_dict = {
                'address': address,
                'balance': balance,
                'transaction_count': transaction_count
            }

        address_info: BitcoinAddress = BitcoinAddress(**address_dict)

        return address_info
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise
