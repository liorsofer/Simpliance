from pymongo.errors import PyMongoError
from logzero import logger
from utils.init_app import container


# generic function to save data to mongodb
def save_to_mongo(data, collection_name):
    try:
        # Use the singleton MongoDB client from the container
        db_client = container.mongo_client()
        db = db_client[container.config.db_schema()]
        collection = db[collection_name]
        collection.insert_one(data)
        logger.info(f"Data saved to MongoDB: {data}")
    except PyMongoError as e:
        logger.error(f"Error saving data to MongoDB: {e}")
    except Exception as e:
        logger.error(f"Unknown error:: {e}")
        raise


# generic function to query one record from mongodb
def get_one_from_mongo(collection_name, query):
    try:
        # Use the singleton MongoDB client from the container
        db_client = container.mongo_client()
        db = db_client[container.config.db_schema()]
        collection = db[collection_name]
        results = collection.find_one(query)
        logger.info(f"Data retrieved from MongoDB: {results}")
        return results
    except PyMongoError as e:
        logger.error(f"Error retrieving data from MongoDB: {e}")
        return None
    except Exception as e:
        logger.error(f"Unknown error:: {e}")
        raise
