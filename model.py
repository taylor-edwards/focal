"""Database schema"""
# pylint: disable=too-few-public-methods

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, Enum, Float, ForeignKey,
    Identity, Integer, String, Table, UniqueConstraint)
from sqlalchemy.sql.functions import now
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

NAME_LENGTH  =   32
TITLE_LENGTH =  100
SHORT_TEXT   =  500
LONG_TEXT    = 2500
Base = declarative_base()

AccountRole = Enum('admin', 'user', name='account_role')
Misbehavior = Enum('other', 'impertinent', 'inappropriate', 'plagiarism', 'impersonation',
                   'harmful', name='misbehavior')
ContentType = Enum('photo', 'edit', 'reply', name='content_type')
ReactionType    = Enum('agree', 'like', 'love', name='reaction_type')
EventType  = Enum('submit_photo', 'submit_edit', 'submit_reply', 'submit_reaction',
                   name='event_type')
EventAssocation = Enum('subject', 'direct_object', 'indirect_object', name='event_association')
Platform        = Enum('Android', 'iOS', 'Linux', 'macOS', 'Windows', name='platform')
MediaCategory   = Enum('photo', 'edit', 'preview', name='media_category')

AccountIdentity      = Identity('Account',      start= 100, cycle=True)
PhotoIdentity        = Identity('Photo',        start= 200, cycle=True)
EditIdentity         = Identity('Edit',         start= 300, cycle=True)
ReplyIdentity        = Identity('Reply',        start= 400, cycle=True)
ReactionIdentity     = Identity('Reaction',     start= 500, cycle=True)
TagIdentity          = Identity('Tag',          start= 600, cycle=True)
ManufacturerIdentity = Identity('Manufacturer', start= 700, cycle=True)
CameraIdentity       = Identity('Camera',       start= 800, cycle=True)
LensIdentity         = Identity('Lens',         start= 900, cycle=True)
EditorIdentity       = Identity('Editor',       start=1000, cycle=True)
PreviewIdentity      = Identity('Preview',      start=1100, cycle=True)
FileIdentity         = Identity('File',         start=1200, cycle=True)
EventIdentity        = Identity('Event',        start=1300, cycle=True)
NotificationIdentity = Identity('Notification', start=1400, cycle=True)
FlagIdentity         = Identity('Flag',         start=1500, cycle=True)
BanIdentity          = Identity('Ban',          start=1600, cycle=True)

# Association tables

"""Which accounts follow which other accounts"""
AccountFollow = Table(
    'account_follow',
    Base.metadata,
    Column('follower_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('following_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))

"""Which accounts are blocking which other accounts"""
AccountBlock = Table(
    'account_block',
    Base.metadata,
    Column('blocker_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('blocked_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))

"""Which accounts have which bans applied to them"""
AccountBan = Table(
    'account_ban',
    Base.metadata,
    Column('account_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('ban_id', ForeignKey('ban.ban_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))

"""Which tags have been applied to which photos"""
PhotoTag = Table(
    'photo_tag',
    Base.metadata,
    Column('photo_id', ForeignKey('photo.photo_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('tag_id', ForeignKey('tag.tag_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True))

"""Which replies are to which photos"""
PhotoReply = Table(
    'photo_reply',
    Base.metadata,
    Column('photo_id', Integer, ForeignKey('photo.photo_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('reply_id', Integer, ForeignKey('reply.reply_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True))

"""Which replies are to which edits"""
EditReply = Table(
    'edit_reply',
    Base.metadata,
    Column('edit_id', Integer, ForeignKey('edit.edit_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('reply_id', Integer, ForeignKey('reply.reply_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True))

"""Which accounts have reacted in which way to which photos"""
PhotoReaction = Table(
    'photo_reaction',
    Base.metadata,
    Column('reaction_id', Integer, ForeignKey('reaction.reaction_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('photo_id', Integer, ForeignKey('photo.photo_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))

"""Which accounts have reacted in which way to which edits"""
EditReaction = Table(
    'edit_reaction',
    Base.metadata,
    Column('reaction_id', Integer, ForeignKey('reaction.reaction_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('edit_id', Integer, ForeignKey('edit.edit_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))

"""Which accounts have reacted in which way to which replies"""
ReplyReaction = Table(
    'reply_reaction',
    Base.metadata,
    Column('reaction_id', Integer, ForeignKey('reaction.reaction_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('reply_id', Integer, ForeignKey('reply.reply_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))

"""Which photos are related to which events"""
PhotoEvent = Table(
    'photo_event',
    Base.metadata,
    Column('photo_id', Integer, ForeignKey('photo.photo_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('event_id', Integer, ForeignKey('event.event_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('event_association', EventAssocation, nullable=False))

"""Which edits are related to which events"""
EditEvent = Table(
    'edit_event',
    Base.metadata,
    Column('edit_id', Integer, ForeignKey('edit.edit_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('event_id', Integer, ForeignKey('event.event_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('event_association', EventAssocation, nullable=False))

"""Which replies are related to which events"""
ReplyEvent = Table(
    'reply_event',
    Base.metadata,
    Column('reply_id', Integer, ForeignKey('reply.reply_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('event_id', Integer, ForeignKey('event.event_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('event_association', EventAssocation, nullable=False))

"""Which reactions are related to which events"""
ReactionEvent = Table(
    'reaction_event',
    Base.metadata,
    Column('reaction_id', Integer, ForeignKey('reaction.reaction_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('event_id', Integer, ForeignKey('event.event_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('event_association', EventAssocation, nullable=False))

"""Who flagged which accounts"""
AccountFlag = Table(
    'account_flag',
    Base.metadata,
    Column('account_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('flagged_account_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('flag_id', ForeignKey('flag.flag_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))

"""Who flagged which photos"""
PhotoFlag = Table(
    'photo_flag',
    Base.metadata,
    Column('account_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('photo_id', ForeignKey('photo.photo_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('flag_id', ForeignKey('flag.flag_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))

"""Who flagged which edits"""
EditFlag = Table(
    'edit_flag',
    Base.metadata,
    Column('account_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('edit_id', ForeignKey('edit.edit_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('flag_id', ForeignKey('flag.flag_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))

"""Who flagged which replies"""
ReplyFlag = Table(
    'reply_flag',
    Base.metadata,
    Column('account_id', ForeignKey('account.account_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('reply_id', ForeignKey('reply.reply_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('flag_id', ForeignKey('flag.flag_id', onupdate='CASCADE',
           ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=now()))




# User created primary content

class Account(Base):
    """Account table"""
    __tablename__ = 'account'
    account_id = Column(Integer, AccountIdentity, primary_key=True)
    account_role = Column(AccountRole, nullable=False, default='user')
    account_name = Column(String(NAME_LENGTH), unique=True, nullable=False)
    account_email = Column(String(SHORT_TEXT), unique=True, nullable=False)
    preview_id = Column(
        Integer,
        ForeignKey('preview.preview_id', onupdate='CASCADE', ondelete='RESTRICT'))
    verified_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=now())
    edited_at = Column(DateTime, nullable=False, onupdate=now(), default=now())
    CheckConstraint(edited_at >= created_at)
    preview = relationship('Preview', uselist=False, cascade='all,delete')
    following = relationship(
        'Account',
        secondary=AccountFollow,
        primaryjoin=account_id == AccountFollow.c.following_id,
        secondaryjoin=account_id == AccountFollow.c.follower_id,
        backref='followers')
    blocked = relationship(
        'Account',
        secondary=AccountBlock,
        primaryjoin=account_id == AccountBlock.c.blocked_id,
        secondaryjoin=account_id == AccountBlock.c.blocker_id,
        backref='blocked_by')
    bans = relationship(
        'Ban',
        secondary=AccountBan,
        backref='accounts',
        cascade='all,delete')
    flags = relationship(
        'Flag',
        secondary=AccountFlag,
        backref='accounts',
        primaryjoin=account_id == AccountFlag.c.flagged_account_id,
        cascade='all,delete')
    reactions = relationship('Reaction', backref='account', cascade='all,delete')

class Photo(Base):
    """Photo table"""
    __tablename__ = 'photo'
    photo_id = Column(Integer, PhotoIdentity, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id', onupdate='CASCADE',
                        ondelete='CASCADE'), nullable=False)
    file_id = Column(Integer, ForeignKey('file.file_id', onupdate='CASCADE',
                     ondelete='RESTRICT'))
    preview_id = Column(Integer, ForeignKey('preview.preview_id', onupdate='CASCADE',
                        ondelete='RESTRICT'))
    camera_id = Column(Integer, ForeignKey('camera.camera_id', onupdate='CASCADE',
                       ondelete='RESTRICT'))
    lens_id = Column(Integer, ForeignKey('lens.lens_id', onupdate='CASCADE',
                     ondelete='RESTRICT'))
    photo_title = Column(String(TITLE_LENGTH), nullable=False)
    photo_description = Column(String(LONG_TEXT), nullable=False)
    aperture = Column(Float)
    flash = Column(Boolean)
    focal_length = Column(Float)
    iso = Column(Integer)
    shutter_speed_denominator = Column(Integer)
    shutter_speed_numerator = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=now())
    edited_at = Column(DateTime, nullable=False, onupdate=now(), default=now())
    CheckConstraint(file_id is not None or preview_id is not None)
    CheckConstraint(photo_title is not None or photo_description is not None)
    CheckConstraint(aperture > 0)
    CheckConstraint(focal_length > 0)
    CheckConstraint(iso > 0)
    CheckConstraint(shutter_speed_denominator > 0)
    CheckConstraint(shutter_speed_numerator > 0)
    CheckConstraint(edited_at >= created_at)
    events = relationship('Event', secondary=PhotoEvent, backref='photos')
    account = relationship('Account', backref='photos', uselist=False)
    file = relationship('File', backref='photo', uselist=False)
    preview = relationship('Preview', backref='photo', uselist=False)
    reactions = relationship('Reaction', secondary=PhotoReaction, backref='photo')
    replies = relationship('Reply', secondary=PhotoReply, backref='photo')
    camera = relationship('Camera', backref='photos')
    lens = relationship('Lens', backref='photos')
    tags = relationship('Tag', secondary=PhotoTag, backref='photos')
    flags = relationship('Flag', secondary=PhotoFlag, backref='photos')

class Edit(Base):
    """Edit table"""
    __tablename__ = 'edit'
    edit_id = Column(Integer, EditIdentity, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id', onupdate='CASCADE',
                        ondelete='CASCADE'), nullable=False)
    file_id = Column(Integer, ForeignKey('file.file_id', onupdate='CASCADE',
                     ondelete='RESTRICT'))
    preview_id = Column(Integer, ForeignKey('preview.preview_id', onupdate='CASCADE',
                        ondelete='RESTRICT'))
    photo_id = Column(Integer, ForeignKey('photo.photo_id', onupdate='CASCADE',
                      ondelete='SET NULL'))
    editor_id = Column(ForeignKey('editor.editor_id', onupdate='CASCADE', ondelete='RESTRICT'))
    edit_title = Column(String(TITLE_LENGTH), nullable=False)
    edit_description = Column(String(LONG_TEXT), nullable=False)
    created_at = Column(DateTime, nullable=False, default=now())
    edited_at = Column(DateTime, nullable=False, onupdate=now(), default=now())
    CheckConstraint(edit_title is not None or edit_description is not None)
    CheckConstraint(edited_at >= created_at)
    events = relationship('Event', secondary=EditEvent, backref='edits')
    account = relationship('Account', backref='edits', uselist=False)
    file = relationship('File', backref='edit', uselist=False)
    preview = relationship('Preview', backref='edit', uselist=False)
    reactions = relationship('Reaction', secondary=EditReaction, backref='edit')
    replies = relationship('Reply', secondary=EditReply, backref='edit')
    photo = relationship('Photo', backref='edits', uselist=False)
    editor = relationship('Editor', backref='edits', uselist=False)
    flags = relationship('Flag', secondary=EditFlag, backref='edits')

class Reply(Base):
    """Reply table"""
    __tablename__ = 'reply'
    reply_id = Column(Integer, ReplyIdentity, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id', onupdate='CASCADE',
                        ondelete='CASCADE'), nullable=False)
    reply_text = Column(String(SHORT_TEXT), nullable=False)
    created_at = Column(DateTime, nullable=False, default=now())
    edited_at = Column(DateTime, nullable=False, onupdate=now(), default=now())
    CheckConstraint(edited_at >= created_at)
    events = relationship('Event', secondary=ReplyEvent, backref='replies')
    account = relationship('Account', backref='replies', uselist=False)
    reactions = relationship('Reaction', secondary=ReplyReaction, backref='reply')
    flags = relationship('Flag', secondary=ReplyFlag, backref='replies')

class Reaction(Base):
    """Reaction table"""
    __tablename__ = 'reaction'
    reaction_id = Column(Integer, ReactionIdentity, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id', onupdate='CASCADE',
                        ondelete='CASCADE'), nullable=False)
    reaction_type = Column(ReactionType, nullable=False, default='agree')
    created_at = Column(DateTime, nullable=False, default=now())
    events = relationship('Event', secondary=ReactionEvent, backref='reaction')

class Preview(Base):
    """Preview table"""
    __tablename__ = 'preview'
    preview_id = Column(Integer, PreviewIdentity, primary_key=True)
    file_id = Column(Integer, ForeignKey('file.file_id', onupdate='CASCADE', ondelete='CASCADE'),
                     nullable=False)
    preview_width = Column(Integer, nullable=False)
    preview_height = Column(Integer, nullable=False)
    CheckConstraint(preview_width > 0)
    CheckConstraint(preview_height > 0)
    file = relationship('File', backref='preview', uselist=False)

class File(Base):
    """File table used to track user uploads"""
    __tablename__ = 'file'
    file_id = Column(Integer, FileIdentity, primary_key=True)
    file_path = Column(String, nullable=False, unique=True)
    file_name = Column(String(TITLE_LENGTH), nullable=False)
    file_extension = Column(String, nullable=False)
    file_size = Column(String, nullable=False)
    media_category = Column(MediaCategory, nullable=False)
    created_at = Column(String, nullable=False)

class Tag(Base):
    """Tag table"""
    __tablename__ = 'tag'
    tag_id = Column(Integer, TagIdentity, primary_key=True)
    tag_name = Column(String(NAME_LENGTH), unique=True, nullable=False)

class Manufacturer(Base):
    """Manufacturer table"""
    __tablename__ = 'manufacturer'
    manufacturer_id = Column(Integer, ManufacturerIdentity, primary_key=True)
    manufacturer_name = Column(String(TITLE_LENGTH), unique=True, nullable=False)

class Camera(Base):
    """Camera table"""
    __tablename__ = 'camera'
    camera_id = Column(Integer, CameraIdentity, primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.manufacturer_id',
        onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    camera_model = Column(String(TITLE_LENGTH), nullable=False)
    UniqueConstraint(camera_model, manufacturer_id)
    manufacturer = relationship('Manufacturer', backref='cameras')

class Lens(Base):
    """Lens table"""
    __tablename__ = 'lens'
    lens_id = Column(Integer, LensIdentity, primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.manufacturer_id',
        onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    lens_model = Column(String(TITLE_LENGTH), nullable=False)
    aperture_min = Column(Float)
    aperture_max = Column(Float)
    focal_length_min = Column(Float)
    focal_length_max = Column(Float)
    CheckConstraint(aperture_min > 0)
    CheckConstraint(aperture_min <= aperture_max)
    CheckConstraint(focal_length_min > 0)
    CheckConstraint(focal_length_min <= focal_length_max)
    UniqueConstraint(lens_model, manufacturer_id)
    manufacturer = relationship('Manufacturer', backref='lenses')

class Editor(Base):
    """Editor table"""
    __tablename__ = 'editor'
    editor_id = Column(Integer, EditorIdentity, primary_key=True)
    editor_name = Column(String(TITLE_LENGTH), nullable=False)
    editor_version = Column(String(20))
    editor_platform = Column(Platform)
    UniqueConstraint(editor_name, editor_version, editor_platform)




# Platform metadata

class Event(Base):
    """
    A list of account interactions with photos, edits, and replies used for feed building.

    Insertion criteria for newly created content:
        * if the creator's account does not have any related bans; then
        * add it to the event feed
    Selection criteria when building events:
        * if the creator's account hasn't appeared in the feed in the last X events; and,
        * any of:
            * if content is a photo; or,
            * if content is an edit and its photo hasn't appeared in the feed
              in the last Y events; or,
            * if content is a reply and its photo hasn't appeared in the feed
              in the last Z events
    """
    __tablename__ = 'event'
    event_id = Column(Integer, EventIdentity, primary_key=True)
    event_type = Column(EventType, nullable=False)
    account_id = Column(Integer, ForeignKey('account.account_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=now())
    account = relationship('Account', backref='events', uselist=False)

class Notification(Base):
    """
    Who has seen which events

    Rows are only inserted for creator accounts' followers at the time of posting
    """
    __tablename__ = 'notification'
    notification_id = Column(Integer, NotificationIdentity, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id', onupdate='CASCADE',
                        ondelete='CASCADE'))
    event_id = Column(Integer, ForeignKey('event.event_id', onupdate='CASCADE',
                      ondelete='CASCADE'))
    created_at = Column(DateTime, nullable=False, default=now())
    viewed_at = Column(DateTime)
    account = relationship('Account', backref='notifications', uselist=False)
    event = relationship('Event', uselist=False)

class Flag(Base):
    """Flag table"""
    __tablename__ = 'flag'
    flag_id = Column(Integer, FlagIdentity, primary_key=True)
    flag_reason = Column(Misbehavior, nullable=False)
    flag_text = Column(String(SHORT_TEXT), nullable=False)
    created_at = Column(DateTime, nullable=False, default=now())

class Ban(Base):
    """Ban table"""
    __tablename__ = 'ban'
    ban_id = Column(Integer, BanIdentity, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=now())
    expires_at = Column(DateTime)
    ban_reason = Column(Misbehavior)
    ban_text = Column(String(SHORT_TEXT), nullable=False)
