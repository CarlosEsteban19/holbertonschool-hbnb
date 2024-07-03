import json
import os

DATA_FILE = "data.json"


def load_storage():
    """Load data from data.json file as dict"""
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            #handle empty data.json
            loaded_data = json.load(f)
            storage = {
                "User": {},
                "Place": {},
                "Review": {},
                "City": {},
                "Country": {},
                "Amenity": {}
            }
            for data_type in storage.keys():
                if data_type in loaded_data:
                    storage[data_type].update(loaded_data[data_type])
        return storage
    return {
        "User": {},
        "Place": {},
        "Review": {},
        "City": {},
        "Country": {},
        "Amenity": {}
        }
    
    
def load_objects():
    """Load data from data.json as objects"""
    objects = {}
    if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                for data_type, items in loaded_data.items():
                    for item, obj_data in items.items():
                        if data_type == "User":
                            from Models.user import User
                            obj = User.from_dict(obj_data)
                        elif data_type == "Place":
                            from Models.place import Place
                            obj = Place.from_dict(obj_data)
                        elif data_type == "Review":
                            from Models.review import Review
                            obj = Review.from_dict(obj_data)
                        elif data_type == "City":
                            from Models.city import City
                            obj = City.from_dict(obj_data)
                        elif data_type == "Amenity":
                            from Models.amenity import Amenity
                            obj = Amenity.from_dict(obj_data)
                            
                        objects[item] = obj

    return objects
    
    


def save_data(data):
    """Save data to data.json file"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


class DataManager():
    """Class to manage all Data and CRUD methods"""

    @classmethod
    def save(cls, identifier, data_type, object):
        """Save Data to storage"""
        storage = load_storage()
        objects = load_objects()
        if data_type not in storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        storage[data_type][identifier] = object.to_dict()
        objects[identifier] = object
        save_data(storage)

    @classmethod
    def get(cls, identifier, data_type):
        """Retrieve Data from storage with given identifier"""
        storage = load_storage()
        objects = load_objects()
        if data_type not in storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        return objects[identifier]

    @classmethod
    def reload(cls, identifier, data_type):
        """Retrieve Data from storage with given identifier"""
        storage = load_storage()
        if data_type not in storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        if identifier not in storage[data_type]:
            return None
        return storage[data_type][identifier]

    @classmethod
    def update(cls, identifier, data_type, object):
        """Update data from storage"""
        storage = load_storage()
        objects = load_objects()
        if data_type not in storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        if identifier in storage[data_type]:
            storage[data_type][identifier] = object.to_dict()
            objects[identifier] = object
            save_data(storage)
        else:
            raise ValueError(f"{data_type} '{identifier}' does not exist")

    @classmethod
    def delete(cls, identifier, data_type):
        """Delete Data from storage with identifier"""
        storage = load_storage()
        objects = load_objects()
        if data_type not in storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        if identifier in storage[data_type]:
            del storage[data_type][identifier]
            save_data(storage)
            del objects[identifier]
        else:
            raise ValueError(f"{data_type} '{identifier}' does not exist")

    @classmethod
    def all(cls, data_type):
        """Retrieve all Data of given Data type"""
        
        storage = load_storage()
        if data_type not in storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        return list(storage[data_type].values())
