from datetime import datetime
from sqlalchemy import \
    Column, create_engine, Date, ForeignKey, Identity, \
    Integer, inspect, MetaData, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base_class = declarative_base()

class Users(base_class):
    __tablename__ = 'users'
    user_id = Column('user_id', Integer, Identity(start=100, cycle=True), primary_key=True)
    user_name = Column('user_name', String, unique=True, nullable=False)
    date_created = Column('date_created', Date, nullable=False)

class Albums(base_class):
    __tablename__ = 'albums'
    album_id = Column('album_id', Integer, Identity(start=200, cycle=True), primary_key=True)
    album_name = Column('album_name', String)
    user_id = Column('user_id', Integer, ForeignKey('users.user_id'))
    date_created = Column('date_created', Date, nullable=False)
    date_edited = Column('date_edited', Date, nullable=False)

class Photos(base_class):
    __tablename__ = 'photos'
    photo_id = Column('photo_id', Integer, Identity(start=300, cycle=True), primary_key=True)
    photo_name = Column('photo_name', String)
    user_id = Column('user_id', Integer, ForeignKey('users.user_id'))
    album_id = Column('album_id', Integer, ForeignKey('albums.album_id'))
    date_created = Column('date_created', Date, nullable=False)
    date_edited = Column('date_edited', Date, nullable=False)
    file_preview = Column('file_preview', String, nullable=False)
    file_source = Column('file_source', String, unique=True, nullable=False)

class Edits(base_class):
    __tablename__ = 'edits'
    edit_id = Column('edit_id', Integer, Identity(start=400, cycle=True), primary_key=True)
    edit_name = Column('edit_name', String)
    user_id = Column('user_id', Integer, ForeignKey('users.user_id'))
    photo_id = Column('photo_id', Integer, ForeignKey('photos.photo_id'))
    date_created = Column('date_created', Date, nullable=False)
    date_edited = Column('date_edited', Date, nullable=False)
    file_preview = Column('file_preview', String, nullable=False)
    file_source = Column('file_source', String, unique=True, nullable=False)

class Database:
    def __init__(self, connection_string):
        self.db = create_engine(connection_string)
        self.__session__ = None
        session = self.create_session()
        base_class.metadata.create_all(self.db)

    def bootstrap(self):
        pass

    def create_session(self):
        if not self.__session__:
            self.create_session = sessionmaker(self.db)
            self.__session__ = self.create_session()
        return self.__session__


    def select_all_users(self):
        return self.create_session().query(Users.user_name)
        # with self.db.connect() as conn:
        #     return conn.execute('SELECT user_name FROM users').mappings().all()

    def insert_users(self, user_name_list):
        with self.db.connect() as conn:
            time = datetime.now().isoformat()
            for user_name in user_name_list:
                statement = self.users.insert().values(
                    user_name=user_name,
                    date_created=time
                )
                conn.execute(statement)

    def delete_users(self, user_name_list):
        with self.db.connect() as conn:
            for user_name in user_name_list:
                statement = self.users.delete().where(self.users.c.user_name == user_name)
                conn.execute(statement)


