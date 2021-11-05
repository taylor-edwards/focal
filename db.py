from sqlalchemy.sql.func import now
from sqlalchemy import Column, create_engine, DateTime, ForeignKey, Identity, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.types import Enum

base_class = declarative_base()

Permission = Enum('none', 'read', 'write', 'delete', name='permission')

Contributor = Enum(
    'other', 'assistant', 'model', 'technician', 'editor', 'photographer', 'director'
    name='contributor'
)

class Account(base_class):
    __tablename__ = 'account'
    account_id = Column(
        'account_id',
        Integer,
        Identity(start=100, cycle=True),
        primary_key=True
    )
    account_name = Column('account_name', String(32), unique=True, nullable=False)
    created_at = Column('created_at', DateTime, nullable=False, default=now())
    edited_at = Column('edited_at', DateTime, nullable=False, onupdate=now())
    deleted_at = Column('deleted_at', DateTime)

class Photo(base_class):
    __tablename__ = 'photo'
    photo_id = Column(
        'photo_id',
        Integer,
        Identity(start=300, cycle=True),
        primary_key=True
    )
    owner_id = Column(
        'owner_id',
        Integer,
        ForeignKey('account.account_id', ondelete='CASCADE', onupdate='CASCADE')
        nullable=False
    )
    photo_name = Column('photo_name', String(32))
    photo_desc = Column('photo_desc', String)
    file_preview = Column('file_preview', String, unique=True, nullable=False)
    file_source = Column('file_source', String, unique=True, nullable=False)
    created_at = Column('created_at', DateTime, nullable=False, default=now())
    edited_at = Column('edited_at', DateTime, nullable=False, onupdate=now())

class Edit(base_class):
    __tablename__ = 'edit'
    edit_id = Column(
        'edit_id',
        Integer,
        Identity(start=400, cycle=True),
        primary_key=True
    )
    photo_id = Column(
        'photo_id',
        Integer,
        ForeignKey('photo.photo_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
    owner_id = Column(
        'owner_id',
        Integer,
        ForeignKey('account.account_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
    edit_name = Column('edit_name', String(32))
    edit_desc = Column('edit_desc', String)
    edit_tool = Column('edit_tool', String(32))
    file_preview = Column('file_preview', String, nullable=False)
    file_source = Column('file_source', String, unique=True, nullable=False)
    created_at = Column('created_at', DateTime, nullable=False, default=now())
    edited_at = Column('edited_at', DateTime, nullable=False, onupdate=now())

class Album(base_class):
    __tablename__ = 'album'
    album_id = Column(
        'album_id',
        Integer,
        Identity(start=200, cycle=True),
        primary_key=True
    )
    owner_id = Column(
        'account_id'
        Integer,
        ForeignKey('account.account_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )
    album_name = Column('album_name', String(32))
    album_desc = Column('album_desc', String)
    created_at = Column('created_at', DateTime, nullable=False, default=now())
    edited_at = Column('edited_at', DateTime, nullable=False, onupdate=now())

class PhotoContributor(base_class):
    __tablename__ = 'photo_contributor'
    account_id = Column(
        'account_id',
        Integer,
        ForeignKey('account.account_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    photo_id = Column(
        'photo_id',
        Integer,
        ForeignKey('photo.photo_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    contributor = Column('contributor', Contributor, nullable=False, default='photographer')
    priority = Column('priority', Integer, nullable=False, default=0)

class EditContributor(base_class):
    __tablename__ = 'edit_contributor'
    account_id = Column(
        'account_id',
        Integer,
        ForeignKey('account.account_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    edit_id = Column(
        'edit_id',
        Integer,
        ForeignKey('edit.edit_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    contributor = Column('contributor', Contributor, nullable=False, default='editor')
    priority = Column('priority', Integer, nullable=False, default=0)

class AlbumAccess(base_class):
    __tablename__ = 'album_access'
    account_id = Column(
        'account_id',
        Integer,
        ForeignKey('account.account_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    album_id = Column(
        'album_id',
        Integer,
        ForeignKey('album.album_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    permission = Column('permission', Permission, nullable=False, default='none')

class AlbumOrder(base_class):
    __tablename__ = 'album_order'
    album_id = Column(
        'album_id',
        Integer,
        ForeignKey('album.album_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    edit_id = Column(
        'edit_id',
        Integer,
        ForeignKey('edit.edit_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    priority = Column('priority', Integer, nullable=False, default=0)

class Tag(base_class):
    __tablename__ = 'tag'
    tag_id = Column(
        'tag_id',
        Integer,
        Identity(start=200, cycle=True),
        primary_key=True
    )
    tag_name = Column('tag_name', String(24), unique=True, nullable=False)
    created_at = Column('created_at', DateTime, nullable=False, default=now())

class PhotoTag(base_class):
    __tablename__ = 'photo_tag'
    tag_id = Column(
        'tag_id',
        Integer,
        ForeignKey('tag.tag_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    photo_id = Column(
        'photo_id',
        Integer,
        ForeignKey('photo.photo_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )

class EditTag(base_class):
    __tablename__ = 'edit_tag'
    tag_id = Column(
        'tag_id',
        Integer,
        ForeignKey('tag.tag_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    edit_id = Column(
        'edit_id',
        Integer,
        ForeignKey('edit.edit_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )

class AlbumTag(base_class):
    __tablename__ = 'album_tag'
    tag_id = Column(
        'tag_id',
        Integer,
        ForeignKey('tag.tag_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    album_id = Column(
        'album_id',
        Integer,
        ForeignKey('album.album_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )

class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        base_class.metadata.create_all(self.engine)

    def select_all_accounts(self):
        with Session(self.engine) as session:
            return session.query(Account).all()

    def select_account(self, account_id):
        with Session(self.engine) as session:
            return session.query(Account).filter_by(account_id=account_id).first()

    def insert_accounts(self, account_name_list):
        with Session(self.engine) as session:
            for account_name in account_name_list:
                account = session.query(Account).filter_by(account_name=account_name).first()
                if account == None:
                    session.add(Account(account_name=account_name))
            session.commit()
            return session.query(Account.account_id).filter(
                Account.account_name.in_(account_name_list)
            ).all()

    def update_account_name(self, account_id, account_name):
        with Session(self.engine) as session:
            session.query(Account).filter(Account.account_id == account_id).update({
                'account_name': account_name,
                'edited_at': now()
            })
            session.commit()

    def delete_accounts(self, account_id_list):
        with Session(self.engine) as session:
            deleted_accounts = []
            for account_id in account_id_list:
                account = self.select_account(account_id)
                if account != None:
                    session.delete(account)
                    deleted_accounts.append(account_id)
            session.commit()
            return deleted_accounts

    def select_album(self, album_id):
        with Session(self.engine) as session:
            return session.query(Album).filter_by(album_id=album_id).first()

    def select_account_albums(self, account_id):
        with Session(self.engine) as session:
            return session.query(Album).filter_by(account_id=account_id).all()

    def insert_albums(self, album_name_list, account_id):
        with Session(self.engine) as session:
            for album_name in album_name_list:
                album = session.query(Album.album_name).filter_by(
                    account_id=account_id,
                    album_name=album_name
                ).first()
                if album == None:
                    session.add(Album(album_name=album_name, account_id=account_id))
            session.commit()
            return (
                session
                .query(Album.album_id)
                .filter_by(account_id=account_id)
                .filter(Album.album_name.in_(album_name_list))
                .all()
            )

    def update_album_name(self, album_id, album_name):
        with Session(self.engine) as session:
            session.query(Album).filter(Album.album_id == album_id).update({
                'album_name': album_name,
                'edited_at': now()
            })
            session.commit()

    def update_album_account_id(self, album_id, account_id):
        with Session(self.engine) as session:
            session.query(Album).filter(Album.album_id == album_id).update({
                'account_id': account_id,
                'edited_at': now()
            })
            session.commit()

    def delete_albums(self, album_id_list):
        with Session(self.engine) as session:
            deleted_albums = []
            for album_id in album_id_list:
                album = self.select_album(album_id)
                if album != None:
                    session.delete(album)
                    deleted_albums.append(album_id)
            session.commit()
            return deleted_albums

    def select_photo(self, photo_id):
        with Session(self.engine) as session:
            return session.query(Photo).filter_by(photo_id=photo_id).first()

    def select_account_photos(self, account_id):
        with Session(self.engine) as session:
            return session.query(Photo).filter_by(account_id=account_id).all()

    def select_album_photos(self, album_id):
        with Session(self.engine) as session:
            return session.query(Photo).filter_by(album_id=album_id).all()

    def insert_photo(self, photo_name, account_id, album_id, file_preview, file_source):
        with Session(self.engine) as session:
            photo_id = session.query(Photo.photo_id).filter_by(file_source=file_source).first()
            if photo_id != None:
                return photo_id

            session.add(Photo(
                photo_name=photo_name,
                account_id=account_id,
                album_id=album_id,
                file_preview=file_preview,
                file_source=file_source
            ))
            session.commit()
            return session.query(Photo.photo_id).filter_by(file_source=file_source).first()

    def update_photo_name(self, photo_id, photo_name):
        with Session(self.engine) as session:
            session.query(Photo).filter(Photo.photo_id == photo_id).update({
                'photo_name': photo_name,
                'edited_at': now()
            })
            session.commit()

    def update_photo_account_id(self, photo_id, account_id):
        with Session(self.engine) as session:
            session.query(Photo).filter(Photo.photo_id == photo_id).update({
                'account_id': account_id,
                'edited_at': now()
            })
            session.commit()

    def update_photo_album_id(self, photo_id, album_id):
        with Session(self.engine) as session:
            session.query(Photo).filter(Photo.photo_id == photo_id).update({
                'album_id': album_id,
                'edited_at': now()
            })
            session.commit()

    def update_photo_files(self, photo_id, file_preview, file_source):
        with Session(self.engine) as session:
            session.query(Photo).filter(Photo.photo_id == photo_id).update({
                'file_preview': file_preview,
                'file_source': file_source,
                'edited_at': now()
            })
            session.commit()

    def select_edit(self, edit_id):
        with Session(self.engine) as session:
            return session.query(Edit).filter_by(edit_id=edit_id).first()

    def select_account_edits(self, account_id):
        with Session(self.engine) as session:
            return session.query(Edit).filter_by(account_id=account_id).all()

    def select_photo_edits(self, photo_id):
        with Session(self.engine) as session:
            return session.query(Edit).filter_by(photo_id=photo_id).all()

    def insert_edit(self, edit_name, account_id, photo_id, file_preview, file_source):
        with Session(self.engine) as session:
            edit_id = session.query(Edit.edit_id).filter_by(file_source=file_source).first()
            if edit_id != None:
                return edit_id

            session.add(Edit(
                edit_name=edit_name,
                account_id=account_id,
                photo_id=photo_id,
                file_preview=file_preview,
                file_source=file_source
            ))
            session.commit()
            return session.query(Edit.edit_id).filter_by(file_source=file_source).first()

    def update_edit_name(self, edit_id, edit_name):
        with Session(self.engine) as session:
            session.query(Edit).filter(Edit.edit_id == edit_id).update({
                'edit_name': edit_name,
                'edited_at': now()
            })
            session.commit()

    def update_edit_account_id(self, edit_id, account_id):
        with Session(self.engine) as session:
            session.query(Edit).filter(Edit.edit_id == edit_id).update({
                'account_id': account_id,
                'edited_at': now()
            })
            session.commit()

    def update_edit_files(self, edit_id, file_preview, file_source):
        with Session(self.engine) as session:
            session.query(Edit).filter(Edit.edit_id == edit_id).update({
                'file_preview': file_preview,
                'file_source': file_source,
                'edited_at': now()
            })
            session.commit()
