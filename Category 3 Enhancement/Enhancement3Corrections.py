from pymongo import MongoClient
from bson.objectid import ObjectId
from cerberus import Validator
import logging

# Configure logging for application-level events
logging.basicConfig(
    filename='animal_shelter.log',  # Log file location
    level=logging.INFO,            # Log level set to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format with timestamp
)

class AnimalShelter:
    """
    CRUD operations for Animal collection in MongoDB.
    Implements robust data validation, logging, and authentication mechanisms.
    """

    def __init__(self, USER, PASS):
        """
        Initialize the MongoDB client with authentication and connection pooling.
        Parameters:
            USER (str): Username for MongoDB authentication.
            PASS (str): Password for MongoDB authentication.
        """
        HOST = 'nv-desktop-services.apporto.com'  # Host address of the MongoDB server
        PORT = 30303                              # Port number for MongoDB
        DB = 'aac'                                # Database name
        COL = 'animals'                           # Collection name

        # Authenticate user credentials
        if not self.authenticate(USER, PASS):
            raise Exception("Authentication failed")  # Raise error if authentication fails

        # MongoClient supports **connection pooling**, which improves resource management and performance
        self.client = MongoClient(
            f'mongodb://{USER}:{PASS}@{HOST}:{PORT}',
            maxPoolSize=50,           # Set a pool of 50 connections for concurrent access
            socketTimeoutMS=30000     # Set a 30-second socket timeout to prevent hanging connections
        )
        self.database = self.client[DB]           # MongoDB database; efficient for hierarchical data
        self.collection = self.database[COL]      # MongoDB collection; stores documents as flexible JSON-like objects
        logging.info("Connection successful.")    # Log successful connection

    def authenticate(self, user, password):
        """
        Simulates user authentication. Replace with a secure mechanism in production.
        Parameters:
            user (str): Username provided by the user.
            password (str): Password provided by the user.
        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        # Example hardcoded authentication logic for demonstration
        return user == "admin" and password == "securepassword"

    def validate_data(self, data):
        """
        Validate input data against a defined schema using the Cerberus library.
        Parameters:
            data (dict): Input data to be validated.
        Returns:
            bool: True if data passes validation, False otherwise.
        """
        
        schema = {
            'name': {'type': 'string', 'minlength': 1, 'regex': '^[a-zA-Z]+$'},  # Name must be alphabetic
            'breed': {'type': 'string', 'minlength': 1, 'regex': '^[a-zA-Z]+$'}, # Breed must be alphabetic
            'age': {'type': 'integer', 'min': 0}                                 # Age must be a non-negative integer
        }
        validator = Validator(schema)  # Validator object for enforcing schema constraints
        return validator.validate(data)  # Validates input in O(n) where n is the number of fields in the schema

    def log_event(self, level, message):
        """
        Log application events at various severity levels.
        Parameters:
            level (str): Severity level ('INFO', 'WARNING', 'ERROR').
            message (str): Message to be logged.
        """
        # Logs are written to a file and timestamped for traceability
        if level.upper() == "INFO":
            logging.info(message)
        elif level.upper() == "WARNING":
            logging.warning(message)
        elif level.upper() == "ERROR":
            logging.error(message)

    def create(self, data, user):
        """
        Insert a new document into the MongoDB collection.
        Parameters:
            data (dict): Data to be inserted into the collection.
            user (str): Username of the user performing the operation.
        Returns:
            bool: True if insertion is successful, False otherwise.
        """
        if self.validate_data(data):  # Validate the input data in O(n) where n is the schema size
            try:
                # MongoDB insertions are O(1) for unindexed collections
                self.collection.insert_one(data)
                self.log_event("INFO", f"User {user} created a record: {data}")
                return True
            except Exception as e:
                self.log_event("ERROR", f"Failed to insert data: {e}")
                return False
        else:
            self.log_event("WARNING", "Validation failed.")
            return False

    def read(self, searchData):
        """
        Query the collection for documents matching the search criteria.
        Parameters:
            searchData (dict): Query criteria.
        Returns:
            list: A list of documents matching the criteria.
        """
        try:
            # MongoDB uses indexed B-trees for queries, providing O(log n) time complexity for indexed fields.
            cursor = self.collection.find(searchData)
            results = list(cursor)  # Convert cursor to a list; may take O(n) for large results
            self.log_event("INFO", f"Read operation successful. Found {len(results)} results.")
            return results
        except Exception as e:
            self.log_event("ERROR", f"Error occurred in read operation: {e}")
            return []

    def update(self, filter, updateData):
        """
        Update existing documents in the collection based on a filter.
        Parameters:
            filter (dict): Criteria to identify documents to be updated.
            updateData (dict): Data to update in matching documents.
        Returns:
            int: Number of documents modified.
        """
        if filter is not None and updateData is not None:  # Ensure both filter and update data are provided
            try:
                # Updates use MongoDB's B-tree indexing for efficient lookups (O(log n))
                update_result = self.collection.update_many(filter, {"$set": updateData})  # Update many matching documents
                modified_count = update_result.modified_count  # Count of modified documents
                self.log_event("INFO", f"Update operation successful. Modified {modified_count} documents.")
                return modified_count
            except Exception as e:
                self.log_event("ERROR", f"Error occurred in update operation: {e}")
                return 0
        else:
            raise Exception("Update failed, filter or updateData parameters are missing")

    def delete(self, filter):
        """
        Delete documents from the collection matching the filter criteria.
        Parameters:
            filter (dict): Criteria to identify documents to be deleted.
        Returns:
            int: Number of documents deleted.
        """
        if filter is not None:  # Ensure filter is provided
            try:
                # Deletions also use indexed lookups for filtering, providing O(log n) efficiency
                delete_result = self.collection.delete_many(filter)  # Delete all matching documents
                deleted_count = delete_result.deleted_count  # Count of deleted documents
                self.log_event("INFO", f"Delete operation successful. Deleted {deleted_count} documents.")
                return deleted_count
            except Exception as e:
                self.log_event("ERROR", f"Error occurred in delete operation: {e}")
                return 0
        else:
            raise Exception("Delete failed, filter parameter is missing")