"""Database schema"""

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Enum, Float, ForeignKey, \
    Identity, Integer, String, Table, UniqueConstraint
from sqlalchemy.sql.functions import now
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

NAME_LENGTH  =   32
TITLE_LENGTH =  100
SHORT_TEXT   =  500
LONG_TEXT    = 2500
Base = declarative_base()

AccountRole = Enum('admin', 'user', name='account_role')

Misbehavior = Enum(
    'other',
    'impertinent',
    'inappropriate',
    'plagiarism',
    'impersonation',
    'harmful',
    name='misbehavior'
)

Platform = Enum(
    'Android',
    'iOS',
    'Linux',
    'macOS',
    'Windows',
    name='platform'
)

NotifyReason = Enum('replied', 'submitted_edit', 'upvoted', name='notify_reason')

ReadStatus = Enum('unread', 'read', name='read_status')

AccountIdentity      = Identity('Account',      start= 100, cycle=True)
PhotoIdentity        = Identity('Photo',        start= 200, cycle=True)
EditIdentity         = Identity('Edit',         start= 300, cycle=True)
ReplyIdentity        = Identity('Reply',        start= 400, cycle=True)
UpvoteIdentity       = Identity('Upvote',       start= 500, cycle=True)
TagIdentity          = Identity('Tag',          start= 600, cycle=True)
EditorIdentity       = Identity('Editor',       start= 700, cycle=True)
CameraIdentity       = Identity('Camera',       start= 800, cycle=True)
LensIdentity         = Identity('Lens',         start= 900, cycle=True)
ManufacturerIdentity = Identity('Manufacturer', start=1000, cycle=True)
PreviewIdentity      = Identity('Preview',      start=1100, cycle=True)
NotificationIdentity = Identity('Notification', start=1200, cycle=True)
FlagIdentity         = Identity('Flag',         start=1300, cycle=True)
BanIdentity          = Identity('Ban',          start=1400, cycle=True)

class Notification(Base):
    """Notification table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'notification'
    notification_id = Column(Integer, NotificationIdentity, primary_key=True)
    recipient_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    actor_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    target_photo_id = Column(
        Integer,
        ForeignKey('photo.photo_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    target_edit_id = Column(
        Integer,
        ForeignKey('edit.edit_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    target_reply_id = Column(
        Integer,
        ForeignKey('reply.reply_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    created_edit_id = Column(
        Integer,
        ForeignKey('edit.edit_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    created_reply_id = Column(
        Integer,
        ForeignKey('reply.reply_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    notify_reason = Column(NotifyReason, nullable=False)
    read_status = Column(ReadStatus, nullable=False, default='unread')
    created_at = Column(DateTime, nullable=False, default=now())
    CheckConstraint(recipient_id is not actor_id)
    CheckConstraint(
        # pylint: disable=literal-comparison
        (target_photo_id is not None) + (target_edit_id is not None) == 1
    )
    CheckConstraint(
        # pylint: disable=literal-comparison
        (created_edit_id is not None) + (created_reply_id is not None) == 1
    )
    recipient = relationship('Account', foreign_keys=recipient_id, back_populates='notifications')
    actor = relationship('Account', foreign_keys=actor_id)
    target_photo = relationship('Photo', foreign_keys=target_photo_id)
    target_edit = relationship('Edit', foreign_keys=target_edit_id)
    target_reply = relationship('Reply', foreign_keys=target_reply_id)
    created_edit = relationship('Edit', foreign_keys=created_edit_id)
    created_reply = relationship('Reply', foreign_keys=created_reply_id)

AccountFollow = Table(
    'account_follow',
    Base.metadata,
    Column('follower_id', ForeignKey('account.account_id'), primary_key=True),
    Column('following_id', ForeignKey('account.account_id'), primary_key=True)
)

AccountBlock = Table(
    'account_block',
    Base.metadata,
    Column('blocker_id', ForeignKey('account.account_id'), primary_key=True),
    Column('blocked_id', ForeignKey('account.account_id'), primary_key=True)
)

AccountBan = Table(
    'account_ban',
    Base.metadata,
    Column('account_id', ForeignKey('account.account_id'), primary_key=True),
    Column('ban_id', ForeignKey('ban.ban_id'), primary_key=True)
)

class Account(Base):
    """Account table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'account'
    account_id = Column(Integer, AccountIdentity, primary_key=True)
    account_role = Column(AccountRole, nullable=False, default='user')
    account_name = Column(String(NAME_LENGTH), unique=True, nullable=False)
    account_email = Column(String(SHORT_TEXT), unique=True, nullable=False)
    # preview_id = Column(
    #     Integer,
    #     ForeignKey('preview.preview_id', onupdate='CASCADE', ondelete='RESTRICT')
    # )
    verified_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=now())
    edited_at = Column(DateTime, onupdate=now())
    CheckConstraint(edited_at > created_at)
    photos = relationship('Photo', back_populates='account', cascade='all, delete')
    edits = relationship('Edit', back_populates='account', cascade='all, delete')
    replies = relationship('Reply', back_populates='account', cascade='all, delete')
    upvotes = relationship('Upvote', back_populates='account', cascade='all, delete')
    # preview = relationship('Preview', uselist=False)
    following = relationship(
        'Account',
        secondary=AccountFollow,
        primaryjoin=account_id == AccountFollow.c.following_id,
        secondaryjoin=account_id == AccountFollow.c.follower_id,
        backref='followers',
        cascade='all, delete'
    )
    notifications = relationship(
        'Notification',
        primaryjoin=account_id == Notification.recipient_id,
        back_populates='recipient',
        cascade='all, delete'
    )
    blocked = relationship(
        'Account',
        secondary=AccountBlock,
        primaryjoin=account_id == AccountBlock.c.blocked_id,
        secondaryjoin=account_id == AccountBlock.c.blocker_id,
        backref='blocked_by',
        cascade='all, delete'
    )
    bans = relationship(
        'Ban',
        secondary=AccountBan,
        back_populates='accounts',
        cascade='all, delete'
    )

class Ban(Base):
    """Ban table"""
    # pylint: disable=too-few-public-methods
    __tablename__ = 'ban'
    ban_id = Column(Integer, BanIdentity, primary_key=True)
    banned_at = Column(DateTime)
    banned_until = Column(DateTime)
    ban_reason = Column(Misbehavior)
    ban_text = Column(String(SHORT_TEXT))
    accounts = relationship('Account', secondary=AccountBan, back_populates='bans')

class Manufacturer(Base):
    """Manufacturer table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'manufacturer'
    manufacturer_id = Column(Integer, ManufacturerIdentity, primary_key=True)
    manufacturer_name = Column(String(TITLE_LENGTH), unique=True, nullable=False)
    cameras = relationship('Camera', back_populates='manufacturer')
    lenses = relationship('Lens', back_populates='manufacturer')

class Camera(Base):
    """Camera table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'camera'
    camera_id = Column(Integer, CameraIdentity, primary_key=True)
    manufacturer_id = Column(
        Integer,
        ForeignKey('manufacturer.manufacturer_id', onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
    )
    camera_model = Column(String(TITLE_LENGTH), nullable=False)
    UniqueConstraint(camera_model, manufacturer_id)
    manufacturer = relationship('Manufacturer', back_populates='cameras')
    photos = relationship('Photo', back_populates='camera')

class Lens(Base):
    """Lens table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'lens'
    lens_id = Column(Integer, LensIdentity, primary_key=True)
    manufacturer_id = Column(
        Integer,
        ForeignKey('manufacturer.manufacturer_id', onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
    )
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
    manufacturer = relationship('Manufacturer', back_populates='lenses')
    photos = relationship('Photo', back_populates='lens')

class Editor(Base):
    """Editor table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'editor'
    editor_id = Column(Integer, EditorIdentity, primary_key=True)
    editor_name = Column(String(TITLE_LENGTH), nullable=False)
    editor_version = Column(String(20))
    editor_platform = Column(Platform)
    UniqueConstraint(editor_name, editor_version, editor_platform)
    edits = relationship('Edit', back_populates='editor')

class Preview(Base):
    """Preview table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'preview'
    preview_id = Column(Integer, PreviewIdentity, primary_key=True)
    preview_file_path = Column(String, unique=True, nullable=False)
    preview_file_size = Column(Integer, nullable=False)
    preview_width = Column(Integer, nullable=False)
    preview_height = Column(Integer, nullable=False)
    CheckConstraint(preview_file_size > 0)
    CheckConstraint(preview_width > 0)
    CheckConstraint(preview_height > 0)

PhotoTag = Table(
    'photo_tag',
    Base.metadata,
    Column('photo_id', ForeignKey('photo.photo_id'), primary_key=True),
    Column('tag_id', ForeignKey('tag.tag_id'), primary_key=True)
)

class Photo(Base):
    """Photo table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'photo'
    photo_id = Column(Integer, PhotoIdentity, primary_key=True)
    account_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    preview_id = Column(
        Integer,
        ForeignKey('preview.preview_id', onupdate='CASCADE', ondelete='RESTRICT')
    )
    camera_id = Column(
        Integer,
        ForeignKey('camera.camera_id', onupdate='CASCADE', ondelete='RESTRICT')
    )
    lens_id = Column(
        Integer,
        ForeignKey('lens.lens_id', onupdate='CASCADE', ondelete='RESTRICT')
    )
    photo_title = Column(String(TITLE_LENGTH))
    photo_description = Column(String(LONG_TEXT))
    raw_file_path = Column(String, unique=True, nullable=False)
    raw_file_extension = Column(String(20), nullable=False)
    raw_file_size = Column(Integer, nullable=False)
    raw_width = Column(Integer)
    raw_height = Column(Integer)
    aperture = Column(Float)
    flash = Column(Boolean, nullable=False, default=False)
    focal_length = Column(Float)
    iso = Column(Integer)
    shutter_speed_denominator = Column(Integer)
    shutter_speed_numerator = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=now())
    edited_at = Column(DateTime, onupdate=now())
    CheckConstraint(raw_width > 0)
    CheckConstraint(raw_height > 0)
    CheckConstraint(aperture > 0)
    CheckConstraint(focal_length > 0)
    CheckConstraint(iso > 0)
    CheckConstraint(shutter_speed_denominator > 0)
    CheckConstraint(shutter_speed_numerator > 0)
    CheckConstraint(photo_title is not None or photo_description is not None)
    account = relationship('Account', back_populates='photos', uselist=False)
    preview = relationship('Preview', uselist=False)
    replies = relationship('Reply', back_populates='photo')
    upvotes = relationship('Upvote', back_populates='photo')
    edits = relationship('Edit', back_populates='photo')
    camera = relationship('Camera', back_populates='photos')
    lens = relationship('Lens', back_populates='photos')
    tags = relationship('Tag', secondary=PhotoTag, back_populates='photos')

class Tag(Base):
    """Tag table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'tag'
    tag_id = Column(Integer, TagIdentity, primary_key=True)
    tag_name = Column(String(NAME_LENGTH), unique=True, nullable=False)
    photos = relationship('Photo', secondary=PhotoTag, back_populates='tags')

class Edit(Base):
    """Edit table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'edit'
    edit_id = Column(Integer, EditIdentity, primary_key=True)
    account_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    preview_id = Column(
        Integer,
        ForeignKey('preview.preview_id', onupdate='CASCADE', ondelete='RESTRICT')
    )
    photo_id = Column(
        Integer,
        ForeignKey('photo.photo_id', onupdate='CASCADE', ondelete='SET NULL')
    )
    editor_id = Column(
        ForeignKey('editor.editor_id', onupdate='CASCADE', ondelete='RESTRICT')
    )
    edit_title = Column(String(TITLE_LENGTH))
    edit_description = Column(String(LONG_TEXT))
    edit_file_path = Column(String, unique=True)
    edit_file_extension = Column(String(20))
    edit_file_size = Column(Integer)
    edit_width = Column(Integer)
    edit_height = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=now())
    edited_at = Column(DateTime, onupdate=now())
    CheckConstraint(edit_file_size > 0)
    CheckConstraint(edit_width > 0)
    CheckConstraint(edit_height > 0)
    CheckConstraint(edit_title is not None or edit_description is not None)
    account = relationship('Account', back_populates='edits', uselist=False)
    preview = relationship('Preview', uselist=False)
    replies = relationship('Reply', back_populates='edit')
    upvotes = relationship('Upvote', back_populates='edit')
    photo = relationship('Photo', back_populates='edits')
    editor = relationship('Editor', back_populates='edits', uselist=False)

class Reply(Base):
    """Reply table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'reply'
    reply_id = Column(Integer, ReplyIdentity, primary_key=True)
    account_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    photo_id = Column(
        Integer,
        ForeignKey('photo.photo_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    edit_id = Column(
        Integer,
        ForeignKey('edit.edit_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    reply_text = Column(String(SHORT_TEXT), nullable=False)
    created_at = Column(DateTime, nullable=False, default=now())
    edited_at = Column(DateTime, onupdate=now())
    CheckConstraint(edited_at > created_at)
    CheckConstraint(photo_id is None is not edit_id is None)
    account = relationship('Account', back_populates='replies', uselist=False)
    photo = relationship('Photo', back_populates='replies')
    edit = relationship('Edit', back_populates='replies')
    upvotes = relationship('Upvote', back_populates='reply')

class Upvote(Base):
    """Upvote table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'upvote'
    upvote_id = Column(Integer, UpvoteIdentity, primary_key=True)
    account_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    upvoted_photo_id = Column(
        Integer,
        ForeignKey('photo.photo_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    upvoted_edit_id = Column(
        Integer,
        ForeignKey('edit.edit_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    upvoted_reply_id = Column(
        Integer,
        ForeignKey('reply.reply_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    created_at = Column(DateTime, nullable=False, default=now())
    UniqueConstraint(account_id, upvoted_photo_id, upvoted_edit_id, upvoted_reply_id)
    CheckConstraint(
        # pylint: disable=literal-comparison
        (upvoted_photo_id is not None) +
        (upvoted_edit_id is not None) +
        (upvoted_reply_id is not None) == 1
    )
    account = relationship('Account', back_populates='upvotes')
    photo = relationship('Photo', back_populates='upvotes')
    edit = relationship('Edit', back_populates='upvotes')
    reply = relationship('Reply', back_populates='upvotes')

class Flag(Base):
    """Flag table"""
     # pylint: disable=too-few-public-methods
    __tablename__ = 'flag'
    flag_id = Column(Integer, FlagIdentity, primary_key=True)
    reporter_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    flagged_account_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    flagged_photo_id = Column(
        Integer,
        ForeignKey('photo.photo_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    flagged_edit_id = Column(
        Integer,
        ForeignKey('edit.edit_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    flagged_reply_id = Column(
        Integer,
        ForeignKey('reply.reply_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    flag_reason = Column(Misbehavior, nullable=False)
    flag_text = Column(String(SHORT_TEXT))
    created_at = Column(DateTime, nullable=False, default=now())
    UniqueConstraint(
        reporter_id,
        flagged_account_id,
        flagged_photo_id,
        flagged_edit_id,
        flagged_reply_id
    )
    CheckConstraint(
        # pylint: disable=literal-comparison
        (flagged_account_id is not None) +
        (flagged_photo_id is not None) +
        (flagged_edit_id is not None) +
        (flagged_reply_id is not None) == 1
    )
    reporter = relationship('Account', foreign_keys=reporter_id)
    flagged_account = relationship('Account', foreign_keys=flagged_account_id)
    flagged_photo = relationship('Photo', foreign_keys=flagged_photo_id)
    flagged_edit = relationship('Edit', foreign_keys=flagged_edit_id)
    flagged_reply = relationship('Reply', foreign_keys=flagged_reply_id)
