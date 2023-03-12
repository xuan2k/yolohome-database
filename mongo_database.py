from pymongo import MongoClient
from .entity import *
from .error import DatabaseException

class IOTDatabase():
    def __init__(self):
        
        #Connect to Atlas server
        self.CONNECTION_STRING = "mongodb+srv://yolohome_database:home123456@onlineserver.m1tnrj9.mongodb.net/IOT_database"
        self.client = MongoClient(self.CONNECTION_STRING)

        #Initial a database if it has not created yet
        self.table_name = ["home_list", "device_list", "room_list", "device_logs", "user_list", "usages", "home_owner"]
        self.instance = (User, Device, Home, Room)
        self.database = self.client['IOT_database']

    def add_data(self, object):

        '''Add an object to database'''
        if not isinstance(object, self.instance):
             message = "Unknow entity in this database!"
             raise OperationFailed(message)

        object._add_callback_(self)

    def add_many_data(self, object_list):

        '''Add many object to database'''

        if not isinstance(object_list, list):
            message = "Many of objects must be formed as a list type!"
            raise OperationFailed(message)
        
        for object in object_list:

            if not isinstance(object, self.instance):
                message = "Unknow entity in this database!"
                raise OperationFailed(message)
            
            object._add_callback_(self)

    def remove_data(self, object):
        object._remove_callback_(self)

    def _find_data(self, table, query):
        return self.database[table].find(query)
    
    def _count_data(self, table, query):
        return self.database[table].count_documents(query)

    def _add_data(self, table, data):

        '''Add a data to table'''

        if table in self.table_name:
                self.database[table].insert_one(data)
                print("Added data to table {}".format(table))
        else:
            message = "Unknown table in database: {}".format(table)
            raise DatabaseException(message)

    def _update_data(self, table, query, data):
         pass    
    
    def _remove_data(self, table, data):
        pass
        
    def list_collection_names(self):
        for i in self.database.list_collection_names():
            for j in self.database[i].find():
                    print(j)
            print("EOF")
