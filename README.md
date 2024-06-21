# Simpliance (Bitcoin Info API)

This project provides a simple FastAPI application with two endpoints to fetch Bitcoin transaction and address information from the Blockcypher API. The application can retrieve details about a Bitcoin address or a specific Bitcoin transaction.

## Features

- **Get Bitcoin Address Information**: Fetch balance and transaction count for a given Bitcoin address.
- **Get Bitcoin Transaction Details**: Fetch detailed information about a specific Bitcoin transaction.

## Endpoints

1. **GET /address/{bitcoin_address}**
   - Fetch balance and transaction count for a given Bitcoin address.
   - Example:
     ```bash
     curl -X GET "http://127.0.0.1:5000/address/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
     ```

2. **GET /transaction/{tx_hash}**
   - Fetch detailed information about a specific Bitcoin transaction.
   - Example:
     ```bash
     curl -X GET "http://127.0.0.1:5000/transaction/b6f6991d8acb14b1a2d91458d337d2b8d9c9a01c8bfa1b93c0916b77f4fedb83"
     ```