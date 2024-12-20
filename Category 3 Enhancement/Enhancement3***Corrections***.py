# --------------------------- Logging Configuration --------------------------- #
# Configures logging to record application events, including info, warnings, and errors
import logging

logging.basicConfig(
    filename='animal_shelter.log',  # File where logs are stored
    level=logging.INFO,             # Log all events at INFO level and above
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format includes timestamp, level, and message
)

# --------------------------- Library Imports --------------------------- #
# Import required libraries for MongoDB, data validation, and more
from pymongo import MongoClient
from bson.objectid import ObjectId
from cerberus import Validator


# --------------------------- AnimalShelter Class --------------------------- #
class AnimalShelter:
    """
    CRUD operations for the Animal collection in MongoDB.
    This class integrates data validation, robust logging, authentication, and advanced database features.
    """

    # --------------------------- Initialization --------------------------- #
    def __init__(self, USER, PASS):
        """
        Initializes the MongoDB client with user authentication and connection pooling.
        Sets up indexes for performance optimization.

        Parameters:
            USER (str): Username for MongoDB authentication.
            PASS (str): Password for MongoDB authentication.
        """
        HOST = 'nv-desktop-services.apporto.com'  # MongoDB server address
        PORT = 30303                              # MongoDB server port
        DB = 'aac'                                # Database name
        COL = 'animals'                           # Collection name

        # Authenticate user credentials to determine access level
        role = self.authenticate(USER, PASS)
        if not role:
            raise Exception("Authentication failed")  # Raise exception if authentication fails
        self.role = role  # Store the authenticated user's role for role-based access control

        # Establish connection to MongoDB with a connection pool
        self.client = MongoClient(
            f'mongodb://{USER}:{PASS}@{HOST}:{PORT}',  # Connection string with credentials
            maxPoolSize=50,           # Maximum number of connections in the pool
            socketTimeoutMS=30000     # Timeout to avoid hanging connections
        )
        self.database = self.client[DB]           # Database handle
        self.collection = self.database[COL]      # Collection handle

        # Create indexes to optimize queries
        self.collection.create_index([("name", 1)], unique=True)  # Index on 'name' for uniqueness
        self.collection.create_index([("breed", 1)])             # Index on 'breed' for efficient filtering
        logging.info("Connection successful and indexes created.")  # Log successful connection setup

    # --------------------------- Authentication --------------------------- #
    def authenticate(self, user, password):
        """
        Authenticates the user and assigns a role based on credentials.

        Parameters:
            user (str): Username provided by the client.
            password (str): Password provided by the client.

        Returns:
            str: Role of the authenticated user, or None if authentication fails.
        """
        # Example static user-role mapping for demonstration purposes
        users = {
            "admin": {"password": "securepassword", "role": "admin"},
            "user": {"password": "userpassword", "role": "user"}
        }
        if user in users and users[user]["password"] == password:
            logging.info(f"Authentication successful for user: {user}")
            return users[user]["role"]
        logging.error("Authentication failed.")  # Log failure for audit purposes
        return None

    # --------------------------- Data Validation --------------------------- #
    def validate_data(self, data):
        """
        Validates the input data structure against a predefined schema.

        Uses the Cerberus library for schema enforcement to ensure data consistency.

        Parameters:
            data (dict): The data object to validate.

        Returns:
            bool: True if data passes validation; False otherwise.
        """
        schema = {
            'name': {'type': 'string', 'minlength': 1, 'regex': '^[a-zA-Z]+$'},  # Name: alphabetic and non-empty
            'breed': {'type': 'string', 'minlength': 1, 'regex': '^[a-zA-Z]+$'}, # Breed: alphabetic and non-empty
            'age': {'type': 'integer', 'min': 0}                                 # Age: non-negative integer
        }
        validator = Validator(schema)
        if validator.validate(data):
            return True
        else:
            logging.warning(f"Validation failed: {validator.errors}")  # Log specific validation errors
            return False

    # --------------------------- Logging Events --------------------------- #
    def log_event(self, level, message):
        """
        Logs application events with appropriate severity levels.

        Parameters:
            level (str): Severity level ('INFO', 'WARNING', 'ERROR').
            message (str): Log message.

        Logs are stored in a timestamped format for traceability.
        """
        if level.upper() == "INFO":
            logging.info(message)
        elif level.upper() == "WARNING":
            logging.warning(message)
        elif level.upper() == "ERROR":
            logging.error(message)

    # --------------------------- Create Operation --------------------------- #
    def create(self, data):
        """
        Inserts a new record into the database after validation.

        Parameters:
            data (dict): The record to insert.

        Returns:
            bool: True if the operation is successful; False otherwise.
        """
        if self.validate_data(data):  # Check data against schema
            try:
                self.collection.insert_one(data)  # O(1) insertion for unindexed collections
                self.log_event("INFO", f"Record created: {data}")
                return True
            except Exception as e:
                self.log_event("ERROR", f"Insert operation failed: {e}")
                return False
        else:
            self.log_event("WARNING", "Validation failed during insertion.")
            return False

    # --------------------------- Read Operation --------------------------- #
    def read(self, searchData):
        """
        Queries the database to retrieve records matching the search criteria.

        Parameters:
            searchData (dict): MongoDB filter to find records.

        Returns:
            list: A list of matching documents.
        """
        try:
            cursor = self.collection.find(searchData)  # Query using the MongoDB filter
            results = list(cursor)  # Convert cursor to a list
            self.log_event("INFO", f"Read operation returned {len(results)} records.")
            return results
        except Exception as e:
            self.log_event("ERROR", f"Read operation failed: {e}")
            return []

    # --------------------------- Update Operation --------------------------- #
    def update(self, filter, updateData):
        """
        Updates existing records in the database based on filter criteria.

        Parameters:
            filter (dict): Criteria to find records to update.
            updateData (dict): Fields to update.

        Returns:
            int: Number of documents modified.
        """
        if filter and updateData:
            try:
                result = self.collection.update_many(filter, {"$set": updateData})  # Update operation
                self.log_event("INFO", f"Updated {result.modified_count} records.")
                return result.modified_count
            except Exception as e:
                self.log_event("ERROR", f"Update operation failed: {e}")
                return 0
        else:
            self.log_event("ERROR", "Update operation failed due to missing parameters.")
            return 0

    # --------------------------- Delete Operation --------------------------- #
    def delete(self, filter):
        """
        Deletes records matching the filter criteria.

        Parameters:
            filter (dict): Criteria to identify records to delete.

        Returns:
            int: Number of records deleted.
        """
        if filter:
            try:
                result = self.collection.delete_many(filter)  # Delete operation
                self.log_event("INFO", f"Deleted {result.deleted_count} records.")
                return result.deleted_count
            except Exception as e:
                self.log_event("ERROR", f"Delete operation failed: {e}")
                return 0
        else:
            self.log_event("ERROR", "Delete operation failed due to missing filter.")
            return 0