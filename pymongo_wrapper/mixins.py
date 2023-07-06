"""
This module provides a mixin class for connecting to a MongoDB database using PyMongo.
"""

from .connection import MongoDBConnection


class DBConnectionMixin:
    """
    A mixin class that provides a connection to a MongoDB database and a collection in that database.

    Args:
        collection_name (str): The name of the collection to connect to.
        database_name (str): The name of the database to connect to.
        uri (str): The connection URI to the MongoDB instance.

    Attributes:
        collection: The PyMongo Collection object representing the connected collection.
    """
    def __init__(self, collection_name: str, database_name: str, uri: str) -> None:
        connection = MongoDBConnection(uri)
        db = connection.get_database(database_name)
        self.collection = db[collection_name]
