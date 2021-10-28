from datetime import datetime
from sqlalchemy import \
    Column, create_engine, Date, ForeignKey, Identity, \
    Integer, inspect, MetaData, String, Table

def get_time():
    return datetime.now().isoformat()

class Database:
    def __init__(self, connection_string):
        self.db = create_engine(connection_string)
        self.meta = MetaData(self.db)
        self.__create_users__()
        self.__create_albums__()
        self.__create_photos__()
        self.__create_edits__()

    def __create_users__(self):
        user_id = Column('user_id', Integer, Identity(start=100, cycle=True), primary_key=True)
        user_name = Column('user_name', String, unique=True, nullable=False)
        date_created = Column('date_created', Date, nullable=False)
        self.users = Table(
            'users',
            self.meta,
            user_id,
            user_name,
            date_created
        )

    def __create_albums__(self):
        album_id = Column('album_id', Integer, Identity(start=200, cycle=True), primary_key=True)
        album_name = Column('album_name', String)
        user_id = Column('user_id', Integer, ForeignKey('users.user_id'))
        date_created = Column('date_created', Date, nullable=False)
        date_edited = Column('date_edited', Date, nullable=False)
        self.albums = Table(
            'albums',
            self.meta,
            album_id,
            album_name,
            user_id,
            date_created,
            date_edited
        )

    def __create_photos__(self):
        photo_id = Column('photo_id', Integer, Identity(start=300, cycle=True), primary_key=True)
        photo_name = Column('photo_name', String)
        user_id = Column('user_id', Integer, ForeignKey('users.user_id'))
        album_id = Column('album_id', Integer, ForeignKey('albums.album_id'))
        date_created = Column('date_created', Date, nullable=False)
        date_edited = Column('date_edited', Date, nullable=False)
        file_preview = Column('file_preview', String, nullable=False)
        file_source = Column('file_source', String, unique=True, nullable=False)
        self.photos = Table(
            'photos',
            self.meta,
            photo_id,
            photo_name,
            user_id,
            album_id,
            date_created,
            date_edited,
            file_preview,
            file_source
        )

    def __create_edits__(self):
        edit_id = Column('edit_id', Integer, Identity(start=400, cycle=True), primary_key=True)
        edit_name = Column('edit_name', String)
        user_id = Column('user_id', Integer, ForeignKey('users.user_id'))
        photo_id = Column('photo_id', Integer, ForeignKey('photos.photo_id'))
        date_created = Column('date_created', Date, nullable=False)
        date_edited = Column('date_edited', Date, nullable=False)
        file_preview = Column('file_preview', String, nullable=False)
        file_source = Column('file_source', String, unique=True, nullable=False)
        self.edits = Table(
            'edits',
            self.meta,
            edit_id,
            edit_name,
            user_id,
            photo_id,
            date_created,
            date_edited,
            file_preview,
            file_source
        )

    def bootstrap(self):
        i = inspect(self.db)
        has_users = i.has_table('users')
        has_albums = i.has_table('albums')
        has_photos = i.has_table('photos')
        has_edits = i.has_table('edits')
        if not (has_users and has_albums and has_photos and has_edits):
            with self.db.connect() as conn:
                if not has_users:
                    self.users.create()
                if not has_albums:
                    self.albums.create()
                if not has_photos():
                    self.photos.create()
                if not has_edits():
                    self.edits.create()

    def select_all_users(self):
        with self.db.connect() as conn:
            return conn.execute('SELECT user_name FROM users').mappings().all()

    def insert_users(self, user_name_list):
        with self.db.connect() as conn:
            time = get_time()
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


