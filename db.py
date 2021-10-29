from datetime import datetime
from sqlalchemy import Column, create_engine, Date, ForeignKey, \
    Identity, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base_class = declarative_base()

class User(base_class):
    __tablename__ = 'user'
    user_id = Column('user_id', Integer, Identity(start=100, cycle=True), primary_key=True)
    user_name = Column('user_name', String(24), unique=True, nullable=False)
    date_created = Column('date_created', Date, nullable=False)

class Album(base_class):
    __tablename__ = 'album'
    album_id = Column('album_id', Integer, Identity(start=200, cycle=True), primary_key=True)
    album_name = Column('album_name', String)
    user_id = Column('user_id', Integer, ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'))
    date_created = Column('date_created', Date, nullable=False)
    date_edited = Column('date_edited', Date, nullable=False)

class Photo(base_class):
    __tablename__ = 'photo'
    photo_id = Column('photo_id', Integer, Identity(start=300, cycle=True), primary_key=True)
    photo_name = Column('photo_name', String)
    user_id = Column('user_id', Integer, ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'))
    album_id = Column('album_id', Integer, ForeignKey('album.album_id', ondelete='CASCADE', onupdate='CASCADE'))
    date_created = Column('date_created', Date, nullable=False)
    date_edited = Column('date_edited', Date, nullable=False)
    file_preview = Column('file_preview', String, nullable=False)
    file_source = Column('file_source', String, unique=True, nullable=False)

class Edit(base_class):
    __tablename__ = 'edit'
    edit_id = Column('edit_id', Integer, Identity(start=400, cycle=True), primary_key=True)
    edit_name = Column('edit_name', String)
    user_id = Column('user_id', Integer, ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'))
    photo_id = Column('photo_id', Integer, ForeignKey('photo.photo_id', ondelete='CASCADE', onupdate='CASCADE'))
    date_created = Column('date_created', Date, nullable=False)
    date_edited = Column('date_edited', Date, nullable=False)
    file_preview = Column('file_preview', String, nullable=False)
    file_source = Column('file_source', String, unique=True, nullable=False)

def get_time():
    return datetime.now().isoformat()

class Database:
    def __init__(self, connection_string):
        self.db = create_engine(connection_string)
        self.__session__ = None
        base_class.metadata.create_all(self.db)

    def create_session(self):
        if self.__session__ == None:
            self.create_session = sessionmaker(self.db)
            self.__session__ = self.create_session()
        return self.__session__

    def close_session(self):
        if self.__session__ != None:
            self.__session__.close()
        self.__session__ = None

    def select_all_users(self):
        with self.create_session() as session:
            return session.query(User).all()

    def select_user(self, user_id):
        with self.create_session() as session:
            return session.query(User).filter_by(user_id=user_id).first()

    def select_users_by_name(self, user_name_list):
        with self.create_session() as session:
            return session.query(User.user_id).filter(User.user_name.in_(user_name_list)).all()

    def insert_users(self, user_name_list):
        with self.create_session() as session:
            time = get_time()
            for user_name in user_name_list:
                user = session.query(User).filter_by(user_name=user_name).first()
                if user == None:
                    session.add(User(user_name=user_name, date_created=time))
            session.commit()
            return self.select_users_by_name(user_name_list)

    def delete_users(self, user_id_list):
        with self.create_session() as session:
            deleted_users = []
            for user_id in user_id_list:
                user = self.select_user(user_id)
                if user != None:
                    session.delete(user)
                    deleted_users.append(user_id)
            session.commit()
            return deleted_users

    def select_album(self, album_id):
        with self.create_session() as session:
            return session.query(Album).filter_by(album_id=album_id).first()

    def select_user_albums(self, user_id):
        with self.create_session() as session:
            return session.query(Album).filter_by(user_id=user_id).all()

    def insert_albums(self, album_name_list, user_id):
        with self.create_session() as session:
            time = get_time()
            for album_name in album_name_list:
                album = session.query(Album.album_name).filter_by(user_id=user_id, album_name=album_name).first()
                if album == None:
                    session.add(Album(
                        album_name=album_name,
                        user_id=user_id,
                        date_created=time,
                        date_edited=time
                    ))
            session.commit()
            return (
                session
                .query(Album.album_id)
                .filter_by(user_id=user_id)
                .filter(Album.album_name.in_(album_name_list))
                .all()
            )

    def delete_albums(self, album_id_list):
        with self.create_session() as session:
            deleted_albums = []
            for album_id in album_id_list:
                album = self.select_album(album_id)
                if album != None:
                    session.delete(album)
                    deleted_albums.append(album_id)
            session.commit()
            return deleted_albums

    def select_photo(self, photo_id):
        with self.create_session() as session:
            return session.query(Photo).filter_by(photo_id=photo_id).first()

    def select_user_photos(self, user_id):
        with self.create_session() as session:
            return session.query(Photo).filter_by(user_id=user_id).all()

    def select_album_photos(self, album_id):
        with self.create_session() as session:
            return session.query(Photo).filter_by(album_id=album_id).all()

    def insert_photo(self, photo_name, user_id, album_id, file_preview, file_source):
        with self.create_session() as session:
            photo_id = session.query(Photo.photo_id).filter_by(file_source=file_source).first()
            if photo_id != None:
                return photo_id

            time = get_time()
            session.add(Photo(
                photo_name=photo_name,
                user_id=user_id,
                album_id=album_id,
                date_created=time,
                date_edited=time,
                file_preview=file_preview,
                file_source=file_source
            ))
            session.commit()
            return session.query(Photo.photo_id).filter_by(file_source=file_source).first()

    def select_edit(self, edit_id):
        with self.create_session() as session:
            return session.query(Edit).filter_by(edit_id=edit_id).first()

    def select_user_edits(self, user_id):
        with self.create_session() as session:
            return session.query(Edit).filter_by(user_id=user_id).all()

    def select_photo_edits(self, photo_id):
        with self.create_session() as session:
            return session.query(Edit).filter_by(photo_id=photo_id).all()

    def insert_edit(self, edit_name, user_id, photo_id, file_preview, file_source):
        with self.create_session() as session:
            edit_id = session.query(Edit.edit_id).filter_by(file_source=file_source).first()
            if edit_id != None:
                return edit_id

            time = get_time()
            session.add(Edit(
                edit_name=edit_name,
                user_id=user_id,
                photo_id=photo_id,
                date_created=time,
                date_edited=time,
                file_preview=file_preview,
                file_source=file_source
            ))
            session.commit()
            return session.query(Edit.edit_id).filter_by(file_source=file_source).first()
