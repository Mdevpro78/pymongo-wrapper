"""
This module provides classes for connecting to MongoDB databases using PyMongo. It includes two classes: MongoDBConnection and DjangoMongoDBConnection.

The MongoDBConnection class provides a simple way to connect to a MongoDB database using a URI string. It has a method for getting a specific database by name.

The DjangoMongoDBConnection class is designed to be used with Django projects. It checks if Django is installed and retrieves the MongoDB URI and database name from the Django settings file. If Django is not installed or if the URI and database name are not found in the settings file, it falls back to using a URI provided in the constructor. It also has a method for getting a specific database by name.
"""


from pymongo import MongoClient
from pymongo.database import Database
from typing import Union, Any, Mapping

from .utils import find_package


class MongoDBConnection:
    """
    A class to connect to a MongoDB database using the MongoClient from PyMongo.

    Args:
        uri (str): The connection URI to the MongoDB instance.

    Attributes:
        uri (str): The connection URI to the MongoDB instance.
        client (Optional[MongoClient]): The PyMongo MongoClient object representing the database connection.

    Methods:
        get_database(database_name: str) -> Database[Union[Mapping[str, Any], Any]]:
            Returns a PyMongo Database object for the specified database name. If a connection hasn't been established
            yet, it will first create a MongoClient using the connection URI provided in the constructor.

    """
    def __init__(self, uri: str) -> None:
        self.uri = uri
        self.client = None

    def get_database(self, database_name: str) -> Database[Union[Mapping[str, Any], Any]]:
        if not self.client:
            self.client = MongoClient(self.uri)
        return self.client[database_name]


class DjangoMongoDBConnection:
    """
    A class to connect to a MongoDB database using Django's settings module or a connection URI.

    Args:
        uri (Optional[str]): The connection URI to the MongoDB instance. Default is None.

    Attributes:
        client (Optional[MongoClient]): The PyMongo MongoClient object representing the database connection.
        uri (Optional[str]): The connection URI to the MongoDB instance.
        db_name (str): The name of the database to connect to, obtained through Django's settings module or manually.

    Properties:
        _is_django_installed (bool): Returns True if Django is installed in the current environment.

    Methods:
        get_database_uri(use_django=True) -> str:
            Returns the connection URI to the MongoDB instance. If use_django is True and Django is installed,
            it will attempt to obtain the URI from Django's settings module. Otherwise, it will return the URI passed in
            the constructor.
            
        get_db_name(use_django=True) -> str:
            Returns the name of the database to connect to. If use_django is True and Django is installed,
            it will attempt to obtain the database name from Django's settings module. Otherwise, it will return
            the name set in the constructor or through the set_db_name() method.
            
        get_database(database_name: str) -> Database[Union[Mapping[str, Any], Any]]:
            Returns a PyMongo Database object for the specified database name. If a connection hasn't been established
            yet, it will first create a MongoClient using the connection URI provided by get_database_uri().
    """
    def __init__(self, uri=None, ):
        self.client = None
        self.uri = uri
        self.db_name = self.get_db_name()

    @property
    def _is_django_installed(self) -> bool:
        return find_package('django')

    def get_database_uri(self, use_django=True) -> str:
        if use_django and self._is_django_installed:
            from django.conf import settings
            return settings.DATABASES['mongodb']['URI']
        return self.uri

    def get_db_name(self, use_django=True) -> str:
        if use_django and self._is_django_installed:
            from django.conf import settings
            self.db_name = settings.DATABASES['mongodb']['DB_NAME']
        return self.db_name

    def get_database(self, database_name: str) -> Database[Union[Mapping[str, Any], Any]]:
        if not self.client:
            self.uri = self.get_database_uri()
            self.client = MongoClient(self.uri)
        return self.client[self.db_name]
