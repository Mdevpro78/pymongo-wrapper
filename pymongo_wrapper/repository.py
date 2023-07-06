"""
This module provides classes for interacting with a MongoDB database using PyMongo.

Classes:
    FindRepository: A class that performs find queries on a PyMongo Collection object.
    InsertRepository: A class that performs insert queries on a PyMongo Collection object.
    UpdateRepository: A class that performs update queries on a PyMongo Collection object.
    DeleteRepository: A class that performs delete queries on a PyMongo Collection object.
    QueryRepository: A class that performs aggregation queries on a PyMongo Collection object.
    DBRepository (inherits from DBConnectionMixin): A mixin class that combines a PyMongo connection with the above
        repository classes to provide a more high-level interface for working with a MongoDB database.
    
Dependencies:
    - PyMongo: A Python distribution containing tools for working with MongoDB.
"""


from pymongo.errors import BulkWriteError
from pymongo.cursor import CursorType
from typing import List, Dict, Any, Collection


from .mixins import DBConnectionMixin

class FindRepository:
    """
    A class that performs find queries on a PyMongo Collection object.

    Args:
        collection (Collection): The PyMongo Collection object to perform the queries on.

    Attributes:
        collection (Collection): The PyMongo Collection object to perform the queries on.

    Methods:
        find(query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
            Returns a list of documents in the collection that match the given query dictionary.
            
        filter_query(pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            Runs the given aggregation pipeline on the collection and returns the resulting documents.
    """

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def find(self, query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """
        Returns a list of documents in the collection that match the given query dictionary.

        Args:
            query (Dict[str, Any]): The query criteria to match documents against. Default is an empty dictionary,
                which matches all documents in the collection.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the matching documents in the collection.
        """
        return self.collection.find(query)

    def filter_query(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]] :
        """
        Runs the given aggregation pipeline on the collection and returns the resulting documents.

        Args:
            pipeline (List[Dict[str, Any]]): A list of pipeline stages to apply to the collection.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the resulting documents from the pipeline.
        """
        return self.collection.aggregate(pipeline)


class InsertRepository:
    """
    A class that performs insert queries on a PyMongo Collection object.

    Args:
        collection (Collection): The PyMongo Collection object to perform the queries on.

    Attributes:
        collection (Collection): The PyMongo Collection object to perform the queries on.

    Methods:
        insert_one(document: Dict[str, Any]) -> Any:
            Inserts a single document into the collection and returns its _id field.
            
        insert_many(documents: List[Dict[str, Any]]) -> Any:
            Inserts multiple documents into the collection and returns their _id fields as a list. If any errors occur
            during the bulk write, a BulkWriteError will be raised.
    """

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def insert_one(self, document: Dict[str, Any]) -> Any:
        """
        Inserts a single document into the collection and returns its _id field.

        Args:
            document (Dict[str, Any]): The document to insert into the collection.

        Returns:
            Any: The _id field of the inserted document.
        """
        return self.collection.insert_one(document)

    def insert_many(self, documents: List[Dict[str, Any]]) -> Any:
        """
        Inserts multiple documents into the collection and returns their _id fields as a list. If any errors occur
        during the bulk write, a BulkWriteError will be raised.

        Args:
            documents (List[Dict[str, Any]]): The documents to insert into the collection.

        Returns:
            Any: The _id fields of the inserted documents as a list.
        """
        try:
            return self.collection.insert_many(documents)
        except BulkWriteError as bwe:
            # handle bulk write errors here
            pass


class UpdateRepository:
    """
    A class that performs update queries on a PyMongo Collection object.

    Args:
        collection (Collection): The PyMongo Collection object to perform the queries on.

    Attributes:
        collection (Collection): The PyMongo Collection object toperform the queries on.

    Methods:
        update_one(query: Dict[str, Any], update: Dict[str, Any]) -> Any:
            Updates a single document in the collection that matches the given query dictionary. The update dictionary
            specifies the changes to make to the matched document.
            
        update_many(query: Dict[str, Any], update: Dict[str, Any]) -> Any:
            Updates multiple documents in the collection that match the given query dictionary. The update dictionary
            specifies the changes to make to the matched documents.
            
        upsert(query: Dict[str, Any], update: Dict[str, Any]) -> Any:
            Updates a single document in the collection that matches the given query dictionary. If no matching
            document is found, a new document is inserted using the update dictionary as its contents.
    """

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> Any:
        """
        Updates a single document in the collection that matches the given query dictionary. The update dictionary
        specifies the changes to make to the matched document.

        Args:
            query (Dict[str, Any]): The query criteria to match documents against.
            update (Dict[str, Any]): The changes to make to matching documents.

        Returns:
            Any: A PyMongo UpdateResult object representing the result of the update operation.
        """
        return self.collection.update_one(query, update)

    def update_many(self, query: Dict[str, Any], update: Dict[str, Any]) -> Any:
        """
        Updates multiple documents in the collection that match the given query dictionary. The update dictionary
        specifies the changes to make to the matched documents.

        Args:
            query (Dict[str, Any]): The query criteria to match documents against.
            update (Dict[str, Any]): The changes to make to matching documents.

        Returns:
            Any: A PyMongo UpdateResult object representing the result of the update operation.
        """
        return self.collection.update_many(query, update)

    def upsert(self, query: Dict[str, Any], update: Dict[str, Any]) -> Any:
        """
        Updates a single document in the collection that matches the given query dictionary. If no matching
        document is found, a new document is inserted using the update dictionary as its contents.

        Args:
            query (Dict[str, Any]): The query criteria to match documents against.
            update (Dict[str, Any]): The changes to make to matching documents.

        Returns:
            Any: A PyMongo UpdateResult object representing the result of the upsert operation.
        """
        return self.collection.update_one(query, update, upsert=True)


class DeleteRepository:
    """
    A class that performs delete queries on a PyMongo Collection object.

    Args:
        collection (Collection): The PyMongo Collection object to perform the queries on.

    Attributes:
        collection (Collection): The PyMongo Collection object to perform the queries on.

    Methods:
        delete_one(query: Dict[str, Any]) -> Any:
            Deletes a single document from the collection that matches the given query dictionary.
    """

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def delete_one(self, query: Dict[str, Any]) -> Any:
        """
        Deletes a single document from the collection that matches the given query dictionary.

        Args:
            query (Dict[str, Any]): The query criteria to match documents against.

        Returns:
            Any: A PyMongo DeleteResult object representing the result of the delete operation.
        """
        return self.collection.delete_one(query)


class QueryRepository:
    """
    A class that performs aggregation queries on a PyMongo Collection object.

    Args:
        collection (Collection): The PyMongo Collection object to perform the queries on.

    Attributes:
        collection (Collection): The PyMongo Collection object to perform the queries on.

    Methods:
        aggregate(pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            Runs the given aggregation pipeline on the collection and returns the resulting documents.
            
        aggregate_exhausted(pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]::
            Runs the given aggregation pipeline on the collection and returns the resulting documents using an
            EXHAUST cursor, which can be useful for handling large results sets. Note that this method blocks until
            the cursor is fully exhausted.
    """
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Runs the given aggregation pipeline on the collection and returns the resulting documents.

        Args:
            pipeline (List[Dict[str, Any]]): A list of pipeline stages to apply to the collection.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the resulting documents from the pipeline.
        """
        return self.collection.aggregate(pipeline)

    def aggregate_exhausted(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]] :
        """
        Runs the given aggregation pipeline on the collection and returns the resulting documents using an
        EXHAUST cursor, which can be useful for handling large results sets. Note that this method blocks until
        the cursor is fully exhausted.

        Args:
            pipeline (List[Dict[str, Any]]): A list of pipeline stages to apply to the collection.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the resulting documents from the pipeline.
        """
        return self.collection.aggregate(pipeline, cursor_type=CursorType.EXHAUST)


class DBRepository(DBConnectionMixin):
    """
    A mixin class that combines a PyMongo connection with FindRepository, InsertRepository, UpdateRepository,
    DeleteRepository, and QueryRepository classes to provide a more high-level interface for working with a MongoDB
    database.

    Args:
        collection_name (str): The name of the collection to connect to.
        database_name (str): The name of the database to connect to.
        uri (str): The connection URI to the MongoDB instance.

    Attributes:
        collection: The PyMongo Collection object representing the connected collection.

    Methods:
        find_repo() -> FindRepository:
            Returns a FindRepository object that can perform find queries on the connected collection.
        
        insert_repo() -> InsertRepository:
            Returns an InsertRepository object that can perform insert queries on the connected collection.
            
        update_repo() -> UpdateRepository:
            Returns an UpdateRepository object that can perform update queries on the connected collection.
            
        delete_repo() -> DeleteRepository:
            Returns a DeleteRepository object that can perform delete queries on the connected collection.
            
        query_repo() -> QueryRepository:
            Returns a QueryRepository object that can perform aggregation queries on the connected collection.
    """

    def __init__(self, collection_name: str, database_name: str, uri: str) -> None:
        super().__init__(collection_name, database_name, uri)

    def find_repo(self) -> FindRepository:
        """
        Returns a FindRepository object that can perform find queries on the connected collection.

        Returns:
            FindRepository: A FindRepository object.
        """
        return FindRepository(self.collection)

    def insert_repo(self) -> InsertRepository:
        """
        Returns an InsertRepository object that can perform insert queries on the connected collection.

        Returns:
            InsertRepository: An InsertRepository object.
        """
        return InsertRepository(self.collection)

    def update_repo(self) -> UpdateRepository:
        """
        Returns an UpdateRepository object that can perform update queries on the connected collection.

        Returns:
            UpdateRepository: An UpdateRepository object.
        """
        return UpdateRepository(self.collection)

    def delete_repo(self) -> DeleteRepository:
        """
        Returns a DeleteRepository object that can perform delete queries on the connected collection.

        Returns:
            DeleteRepository: A DeleteRepository object.
        """
        return DeleteRepository(self.collection)

    def query_repo(self) -> QueryRepository:
        """
        Returns a QueryRepository object that can perform aggregation queries on the connected collection.

        Returns:
            QueryRepository: A QueryRepository object.
        """
        return QueryRepository(self.collection)
