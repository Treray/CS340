from bson.objectid import ObjectId
from pymongo import MongoClient, errors
import logging
import os

#TR 10/24/2024

# CRUD module with the AnimalShelter class
class AnimalShelter:
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username='aacuser', password='Tre1990', host=None, port=None, db='AAC', collection='animals', auth_db='admin'):
      
        #Initialize the AnimalShelter class with MongoDB connection parameters
        
        # Fetch environment variables if host and port are not provided
        self.USER = username
        self.PASS = password
        self.HOST = host if host else os.getenv('MONGO_HOST')

        # Check if port is provided and valid, otherwise default to 27017
        if port and isinstance(port, str) and port.isdigit():
            self.PORT = int(port)
        else:
            self.PORT = int(os.getenv('MONGO_PORT', 27017))

        print(f"HOST: {self.HOST}, PORT: {self.PORT}")  #TR 10/24/2024

        self.DB = db
        self.COLLECTION = collection
        self.AUTH_DB = auth_db

        # Construct MongoDB URI
        mongo_uri = f"mongodb://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.AUTH_DB}"

        # Initialize connection
        try:
            self.client = MongoClient(mongo_uri)
            self.database = self.client[self.DB]
            self.collection = self.database[self.COLLECTION]
            logging.info(f"Connected to MongoDB at {self.HOST}:{self.PORT}")
        except errors.PyMongoError as e:
            logging.error(f"Failed to connect to MongoDB at {self.HOST}:{self.PORT}. Error: {e}")
            raise

    def create(self, data):
       
        #Creates a new document in the database.
       
        if data:                                                               #TR 10/24/2024
            try:
                result = self.collection.insert_one(data)
                return {"status": "success", "inserted_id": str(result.inserted_id), "acknowledged": result.acknowledged}
            except errors.PyMongoError as e:
                logging.error(f"Error while inserting data: {e}")
                return {"status": "error", "message": str(e)}
        else:
            raise ValueError("Data cannot be empty")

    def read(self, query=None):
        
        #Searches for documents in the database based on a query
        
        if query is None:
            query = {}  # Default to an empty query to fetch all records
        try:
            results = list(self.collection.find(query))
            return {"status": "success", "data": results}
        except errors.PyMongoError as e:
            logging.error(f"Error while reading data: {e}")
            return {"status": "error", "message": str(e)}
    
    def update(self, query, updated_data):                 #TR 10/24/2024
        
        #Update documents in the database
        
        if query and updated_data:
            try:
                result = self.collection.update_many(query, {"$set": updated_data})
                return {"status": "success", "modified_count": result.modified_count}
            except errors.PyMongoError as e:
                logging.error(f"Error while updating data: {e}")
                return {"status": "error", "message": str(e)}
        else:
            raise ValueError("Query and updated data cannot be empty")

    def delete(self, query):
       
        #Delete documents from the database
        
        if query:
            try:
                result = self.collection.delete_many(query)
                if result.deleted_count > 0:
                    return {"status": "success", "deleted_count": result.deleted_count}
                else:
                    return {"status": "warning", "message": "No documents matched the query, no documents deleted"}
            except errors.PyMongoError as e:
                logging.error(f"Error while deleting data: {e}")
                return {"status": "error", "message": str(e)}
        else:
            raise ValueError("Query cannot be empty")

    def close_connection(self):                           #TR 10/24/2024
        """Close the MongoDB connection."""
        self.client.close()