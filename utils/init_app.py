from dependency_injector import containers, providers
from logzero import logger
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

container = containers.DynamicContainer()


def test_mongodb_connection(client: MongoClient, schema: str):
    try:
        # Attempt to get server info to verify the connection
        client.server_info()
        db = client[schema]
        logger.info(f"Connected to MongoDB, Database: {db.name}")
    except ServerSelectionTimeoutError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    except PyMongoError as e:
        logger.error(f"MongoDB error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unknown error:: {e}")
        raise


def init_application(app_name: str = "Simpliance"):
    """
    env:
        DB_URI: URI to connect to the DB server
        DB_SCHEMA: what schema to use in the DB
    """
    container.config = providers.Configuration()
    container.config.db_uri.from_env("DB_URI", "mongodb://127.0.0.1:27017")
    container.config.db_schema.from_env("DB_SCHEMA", "simpliance")

    # Ensure the configuration values are set correctly
    db_uri = container.config.db_uri()
    db_schema = container.config.db_schema()
    logger.info(f"Config DB_URI: {db_uri}")
    logger.info(f"Config DB_SCHEMA: {db_schema}")

    # MongoDB Singleton
    container.mongo_client = providers.Singleton(
        MongoClient,
        host=db_uri,
        serverSelectionTimeoutMS=5000,  # 5 seconds timeout
        tz_aware=True
    )

    logger.info(f"=====> {app_name} started <===========")
    logger.info(f"  Application: {app_name}==========")
    logger.info(f"  DB:: ({db_uri}, {db_schema})")

    # Test MongoDB connection
    try:
        db_client = container.mongo_client()
        test_mongodb_connection(db_client, db_schema)
    except PyMongoError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Unknown error:: {e}")
        raise
