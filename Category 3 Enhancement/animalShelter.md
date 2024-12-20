from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, USER, PASS):
            # Initializing the MongoClient. This helps to 
            # access the MongoDB databases and collections.
            # This is hard-wired to use the aac database, the 
            # animals collection, and the aac user.
            # Definitions of the connection string variables are
            # unique to the individual Apporto environment.
            #
            # You must edit the connection variables below to reflect
            # your own instance of MongoDB!
            #
            # Connection Variables
            #
            #USER = "aacuser"
            #PASS = "SNHU1234"
            HOST = 'nv-desktop-services.apporto.com'
            PORT = 30303
            DB = 'aac'
            COL = 'animals'
            #
            # Initialize Connection
            #
            self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
            self.database = self.client['%s' % (DB)]
            self.collection = self.database['%s' % (COL)]
            print ("Connection Successful")
            
    #Method to implement the C in CRUD.
    # Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            self.database.animals.insert_one(data) # data should be dictionary
            return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")
    
    #Method to implement the R in CRUD.
    def read(self, searchData):
            """Query for documents from a specified MongoDB database and collection."""
            try:
                cursor = self.collection.find(searchData)
                return list(cursor)
            except Exception as e:
                print(f"Error occurred in read operation: {e}")
                return []
    
    #Method to implement U in CRUD
    def update(self, filter, updateData):
            """Update documents in a specified MongoDB database and collection."""
            if filter is not None and updateData is not None:
                try:
                    update_result = self.collection.update_many(filter, {"$set": updateData})
                    return update_result.modified_count #Shows the amount of documents that have been changed
                except Exception as e:
                    print(f"Error occurred in update operation: {e}")
                    return 0 #If zero is returned an exception has occurred
            else:
                raise Exception("Update failed, filter or updateData parameters are missing")
                
    def update(self, filter, updateData):
            """Update documents in a specified MongoDB database and collection."""
            if filter is not None and updateData is not None:
                try:
                    # Correct use of $set to update fields without replacing the entire document.
                    update_result = self.collection.update_many(filter, {"$set": updateData})
                    return update_result.modified_count  # Shows how many documents were updated
                except Exception as e:
                    print(f"Error occurred in update operation: {e}")
                    return 0  # Return zero if an exception occurred
            else:
                raise ValueError("Update failed, filter or updateData parameters are missing")
    
    #Method to implement D in CRUD
    def delete(self, filter):
            """Delete documents from a specified MongoDB database and collection."""
            if filter is not None:
                try:
                    delete_result = self.collection.delete_many(filter)
                    return delete_result.deleted_count 
                except Exception as e:
                    print(f"Error occurred in delete operation: {e}")
                    return 0
            else:
                raise Exception("Delete failed, filter parameter is missing")

