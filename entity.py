#Entities in system
from .error import *

class User():
    def __init__(self,
                 username = None,
                 password = None,
                 IDimage = None):
        self._username = username
        self._password = password
        self._IDimage = IDimage
        self.data = {}

    def _add_callback_(self, table):
        table._add_data("user_list", self.data)

    def _remove_callback_(self, table):
        table._remove_data(self)
    
    def update(self, field, data):
        pass

class Device():
    def __init__(self,
                 type : str,
                 state : bool = None,                     #0: inactive, 1: active
                 time_activated : str = None,
                 time_deactivated : str = None,
                 value = None,
                 room_id : str = None,
                 home_id : str = None):
        
        self.devices = ["temp_sensor", "humid_sensor", "light_sensor", "movement_sensor", "led", "fan", "door"]
        self.feed_id = {}

        if type not in self.devices:
            message = "Unknown device in this database. Available device are {}".format(i for i in self.devices)
            raise DatabaseException(message)

        self.data = {
            "_id" : self.feed_id,
            "type" : type,
            "state" : state,
            "time_activated" : time_activated,
            "time_deactivate" : time_deactivated,
            "value" : value,
            "room_id" : room_id,
            "home_id" : home_id
        }

    def _add_callback_(self, table):
        query = {"type" : self.data["type"]}
        get_id = table._count_data(table, query)

        if type in ["led", "fan"]:
            self.feed_id["id1"] = "{}.{}{:05d}_state".format(self.data["home_id"], self.data["type"], get_id)
            self.feed_id["id2"] = "{}.{}{:05d}_value".format(self.data["home_id"], self.data["type"], get_id)
        else:
            self.feed_id["id"] = "{}.{}{:05d}".format(self.data["home_id"], self.data["type"])

        self.data["_id"] = self.feed_id

        table._add_data("device_list", self.data)

    def _update_callback(self, table):
        table._update_data(self)

    def _remove_callback_(self, table):
        table._remove_data(self)
    
    def update(self, field, data):
        try:
            if isinstance(data[field], dict) and not isinstance(data, dict):
                message = "Type mismatch between old and new data when update field {}!".format(field)
                raise OperationFailed(message)

            if field in self.data.keys():
                self.data[field] = data
            else:
                message = "Field {} is not available in this table!".format(field)
                raise DatabaseException(message)
        except:
            raise DatabaseException()

class Home():
    def __init__(self):
        pass
    def _add_callback_(self, table):
        table._add_data(self)

    def _remove_callback_(self, table):
        table._remove_data(self)

class Room():
    def __init__(self):
        pass
    def _add_callback_(self, table):
        table._add_data(self)

    def _remove_callback_(self, table):
        table._remove_data(self)

# class TempSensor(Device):
#     def __init__(self,
#                  feed_id,
#                  state,                     #0: inactive, 1: active 
#                  time_activated,
#                  time_deactivated, 
#                  value,
#                  roomID):
#         self.type = "Temperature Sensor"
#         self.value = value
#         super().__init__(self.type)

#     def _add_callback_(self, table):
#         table._add_data(self, self.type)

#     def _remove_callback_(self, table):
#         table._remove_data(self, self.type)

# class HumidSensor(Device):
#     def __init__(self,
#                  feed_id,
#                  state,
#                  time_activated,
#                  time_deactivated, 
#                  value,
#                  roomID):
#         self.type = "Humidity Sensor"
#         super().__init__(self.type)

#     def _add_callback_(self, table):
#         table._add_data(self, self.type)

#     def _remove_callback_(self, table):
#         table._remove_data(self, self.type)

# class LuxSensor(Device):
#     def __init__(self,
#                  feed_id,
#                  state,
#                  time_activated,
#                  time_deactivated, 
#                  value,
#                  roomID):
#         self.type = "Light Sensor"
#         super().__init__(self.type)

#     def _add_callback_(self, table):
#         table._add_data(self, self.type)

#     def _remove_callback_(self, table):
#         table._remove_data(self, self.type)

# class MovementSensor(Device):
#     def __init__(self,
#                  feed_id,
#                  state,
#                  time_activated,
#                  time_deactivated, 
#                  isMovement,
#                  roomID):
#         self.type = "Movement Sensor"
#         super().__init__(self.type)

#     def _add_callback_(self, table):
#         table._add_data(self, self.type)

#     def _remove_callback_(self, table):
#         table._remove_data(self, self.type)

# class Fan(Device):
#     def __init__(self,
#                  feed_id,
#                  state,
#                  time_activated,
#                  time_deactivated, 
#                  speed,
#                  roomID):
#         self.type = "Fan"
#         super().__init__(self.type)

#     def _add_callback_(self, table):
#         table._add_data(self, self.type)

#     def _remove_callback_(self, table):
#         table._remove_data(self, self.type)

# class RGBLed(Device):
#     def __init__(self,
#                  feed_id,
#                  state,                     #0: off, 1: on
#                  time_activated,
#                  time_deactivated,
#                  color,
#                  roomID):
#         self.type = "Led RGB"
#         super().__init__(self.type)

#     def _add_callback_(self, table):
#         table._add_data(self, self.type)

#     def _remove_callback_(self, table):
#         table._remove_data(self, self.type)
