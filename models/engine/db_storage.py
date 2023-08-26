from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv

class DBStorage:
    __engine = None
    __session = None
    classes = {"City": City, "State": State, "Place": Place, "User": User, "Review": Review}
    
    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
            
    def all(self, cls=None):
        objs = {}

        if cls:
            if type(cls) == str:
                cls = self.classes.get(cls)
                for obj in self.__session.query(cls).all():
                    print('test')
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objs[key] = obj
        else:
            for cls in classes.values():
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objs[key] = obj

        return objs

    def new(self, obj):
        self.__session.add(obj)
        
    def save(self):
        self.__session.commit()
        
    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)
            
    def reload(self):
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()
