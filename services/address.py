import requests
from logzero import logger

from models.bitcoin_address import BitcoinAddress
from utils.mongo import save_to_mongo, get_one_from_mongo

# URL to use API for bitcoin addresses from blockcypher
BASE_URL = 'https://api.blockcypher.com/v1/btc/main/addrs/'


# get bitcoin addresses and return details about the address
# also cache the details into mongo (before using blockcypher we also validate if it is not already in cache)
def get_bitcoin_address_info(address) -> BitcoinAddress | None:
    url = f'{BASE_URL}{address}'

    try:
        # is in cache
        data = get_one_from_mongo(collection_name="address_info", query={'address': address})
        if not data:
            # not in cache (mongodb) so we use blockcypher api
            response = requests.get(url)
            if response.status_code == 404:
                logger.error(f"Bitcoin address not found: {address}")
                return None
            response.raise_for_status()  # Raise an error for other bad status codes

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

            # Save to MongoDB (cache the bitcoind address information)
            save_to_mongo(address_dict, collection_name="address_info")
            address_info: BitcoinAddress = BitcoinAddress(**address_dict)

        else:
            address_info: BitcoinAddress = BitcoinAddress(**data)

        return address_info
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise
    except Exception as e:
        logger.error(f"Unknown error:: {e}")
        raise
