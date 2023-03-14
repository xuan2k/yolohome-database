#Entities in system
from .error import *
from datetime import datetime

class User():
    def __init__(self,
                 username = None,
                 password = None,
                 image_id = None,
                 home_id = None):
        
        self.data = {
            "username" : username,
            "password" : password,
            "image_id" : None if image_id is None else [image_id],
            "home_id"  : None if home_id is None else [home_id] 
        }

    def _add_callback_(self, 
                       collection):

        query = {}
        get_id = collection._count_data("user_list", query)
        self.data["_id"] = "user{:05d}".format(get_id)
        collection._add_data("user_list", self.data)

    def _update_callback_(self, 
                         collection, 
                         updated_data, 
                         query = None, 
                         mode = "first"):
        
        if query is None:
            query = {"_id" : self.data["_id"]}
        
        if not isinstance(updated_data, dict):
            message = "Update data must be form as a dictionary!"
            raise OperationFailed(message)

        for k, v in self.data.items():

            if k in updated_data.keys():

                if k == "image_id" or "home_id":

                    if self.data[k] is None:

                        if isinstance(updated_data[k], list):
                            self.data[k] = updated_data[k]

                        else:
                            self.data[k] = [updated_data[k]]

                    else:

                        if isinstance(updated_data[k], list):
                            self.data[k] + updated_data[k]

                        else:
                            self.data[k].append(updated_data[k])

                else:
                    self.data[k] = updated_data[k]


        collection._update_data("user_list", self.data, query, mode)

    def _remove_callback_(self, 
                          collection,
                          query,
                          mode):
        
        collection._remove_data("user_list", query, mode)

    def load_data(self, 
                  load_data : dict):
        
        """Load a data dictionary to object"""

        for k,v in self.data.items():
            if k not in load_data.keys():
                message = "Field {} is not available in the loading data!".format(k)
                raise OperationFailed(message)
            if isinstance(v, dict):
                self.data[k].update(load_data[k])
            elif k in load_data.keys():
                self.data[k] = load_data[k]

    def show(self):
        return self.data

class Device():
    def __init__(self,
                 type : str, 
                 room_id : str = None,
                 home_id : str = None,                   
                 curr_state : bool = None,              #0: inactive, 1: active
                 curr_value = None,
                 time_activated : str = None,
                 time_deactivated : str = None):

        self.devices = ["temp-sensor", "humid-sensor", "light-sensor", "movement-sensor", "led", "fan", "door"]
        self.feed_id = None

        if type not in self.devices:
            message = "Unknown device in this database. Available device are {}".format(i for i in self.devices)
            raise DatabaseException(message)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        self.data = {
            "_id" : self.feed_id,
            "type" : type,
            "room_id" : room_id,
            "home_id" : home_id,
            "states" : {} if curr_state is None else {dt_string : curr_state},
            "curr_state" : curr_state,
            "state_time" : {} if time_activated is None else {time_activated : time_deactivated},
            "values" : {} if curr_value is None else {dt_string : curr_value},
            "curr_value" : curr_value
        }

    def _add_callback_(self, 
                       collection):
        
        query = {"_id" : self.data["home_id"]}
        exist =  collection._count_data("home_list", query)
        if not exist:
            message = "Id not found in database: {}!".format(self.data["home_id"])
            raise DatabaseException(message)
        
        query = {"_id" : self.data["room_id"]}
        exist =  collection._count_data("room_list", query)
        if not exist:
            message = "Id not found in database: {}!".format(self.data["room_id"])
            raise DatabaseException(message)

        query = {"type" : self.data["type"]}
        get_id = collection._count_data("device_list", query)
        
        self.feed_id = "{}{:05d}".format(self.data["type"],get_id)

        self.data["_id"] = self.feed_id

        collection._add_data("device_list", self.data)

    def _update_callback_(self, 
                         collection, 
                         updated_data, 
                         query = None, 
                         mode = "first"):
        
        if query is None:
            query = {"_id" : self.data["_id"]}
        
        if not isinstance(updated_data, dict):
            message = "Update data must be form as a dictionary!"
            raise OperationFailed(message)

        for k, v in self.data.items():

            if k in updated_data.keys():

                if isinstance(v, dict) and isinstance(updated_data[k], dict):
                    self.data[k].update(updated_data[k])

                elif k == "curr_value":
                    self.data[k] = updated_data[k]
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    self.data["values"][dt_string] = updated_data[k]

                elif k == "curr_state":

                    if self.data[k] != updated_data[k]:
                        self.data[k] = updated_data[k]
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        if updated_data[k]:
                            self.data["state_time"][dt_string] = None
                        else:
                            last_ley = list(self.data["state_time"])[-1]
                            self.data["state_time"][last_ley] = dt_string

                else:
                    self.data[k] = updated_data[k]
                
        collection._update_data("device_list", self.data, query, mode)

    def _remove_callback_(self, 
                          collection,
                          query,
                          mode):
        
        collection._remove_data("device_list", query, mode)
    
    
    def load_data(self, 
                  load_data : dict):
        
        """Load a data dictionary to object"""

        for k,v in self.data.items():
            if k not in load_data.keys():
                message = "Field {} is not available in the loading data!".format(k)
                raise OperationFailed(message)
            if isinstance(v, dict):
                self.data[k].update(load_data[k])
            elif k in load_data.keys():
                self.data[k] = load_data[k]

    def show(self):
        return self.data

    def get_log(self):
        return {self.data["states"], self.data["values"]}

class Home():
    def __init__(self,
                 name = None):

        self.data = {
            "name" : name
        }

    def _add_callback_(self, 
                       collection):
        
        query = {}
        get_id = collection._count_data("home_list", query)

        if self.data["name"] is None:
            self.data["name"] = "YoloSmartHome{:05d}".format(get_id)
        
        self.data["_id"] = "home{:05d}".format(get_id)

        collection._add_data("home_list", self.data)

    def _update_callback_(self, 
                         collection, 
                         updated_data, 
                         query = None, 
                         mode = "first"):
        
        if query is None:
            query = {"_id" : self.data["_id"]}
        
        if not isinstance(updated_data, dict):
            message = "Update data must be form as a dictionary!"
            raise OperationFailed(message)

        for k, v in self.data.items():
            if k in updated_data.keys():
                self.data[k] = updated_data[k]

        collection._update_data("home_list", self.data, query, mode)


    def _remove_callback_(self, 
                          collection,
                          query,
                          mode):
        
        collection._remove_data("home_list", query, mode)

    def load_data(self, 
                  load_data : dict):
        
        """Load a data dictionary to object"""

        for k,v in self.data.items():
            if k not in load_data.keys():
                message = "Field {} is not available in the loading data!".format(k)
                raise OperationFailed(message)
            if isinstance(v, dict):
                self.data[k].update(load_data[k])
            elif k in load_data.keys():
                self.data[k] = load_data[k]

    def show(self):
        return self.data

class Room():
    def __init__(self,
                 home_id,
                 name = None):

        self.data = {
            "home_id" : home_id,
            "name" : name
        }

    def _add_callback_(self, 
                       collection):
        
        query = {"_id" : self.data["home_id"]}
        exist =  collection._count_data("home_list", query)
        if not exist:
            message = "Id not found in database: {}!".format(self.data["home_id"])
            raise DatabaseException(message)
        
        query = {}
        get_id = collection._count_data("home_list", query)

        if self.data["name"] is None:
            self.data["name"] = "{}.YoloRoom{:05d}".format(self.data["home_id"], get_id)
        
        self.data["_id"] = "home{:05d}".format(get_id)

        collection._add_data("home_list", self.data)

    def _update_callback_(self, 
                         collection, 
                         updated_data, 
                         query = None, 
                         mode = "first"):
        
        if query is None:
            query = {"_id" : self.data["_id"]}
        
        if not isinstance(updated_data, dict):
            message = "Update data must be form as a dictionary!"
            raise OperationFailed(message)

        for k, v in self.data.items():
            if k in updated_data.keys():
                self.data[k] = updated_data[k]

        collection._update_data("room_list", self.data, query, mode)


    def _remove_callback_(self, 
                          collection,
                          query,
                          mode):
        
        collection._remove_data("room_list", query, mode)

    def load_data(self, 
                  load_data : dict):
        
        """Load a data dictionary to object"""

        for k,v in self.data.items():
            if k not in load_data.keys():
                message = "Field {} is not available in the loading data!".format(k)
                raise OperationFailed(message)
            if isinstance(v, dict):
                self.data[k].update(load_data[k])
            elif k in load_data.keys():
                self.data[k] = load_data[k]

    def show(self):
        return self.data



    # def replace(self, 
    #             field, 
    #             data):
    #     try:
    #         if isinstance(data[field], dict) and not isinstance(data, dict):
    #             message = "Type mismatch between old and new data when update field {}!".format(field)
    #             raise OperationFailed(message)

    #         if field in self.data.keys():
    #             self.data[field] = data
    #         else:
    #             message = "Field {} is not available in this collection!".format(field)
    #             raise DatabaseException(message)
    #     except:
    #         raise DatabaseException()