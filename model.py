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

ACCOUNT_ID_BASE      =  100
PHOTO_ID_BASE        =  200
EDIT_ID_BASE         =  300
REPLY_ID_BASE        =  400
UPVOTE_ID_BASE       =  500
TAG_ID_BASE          =  600
MANUFACTURER_ID_BASE =  700
CAMERA_ID_BASE       =  800
LENS_ID_BASE         =  900
EDITOR_ID_BASE       = 1000
PREVIEW_ID_BASE      = 1100
NOTIFICATION_ID_BASE = 1200
FLAG_ID_BASE         = 1300

Base = declarative_base()

Account_Role = Enum('admin', 'user', name='account_role')

Flag_Reason = Enum(
    'irrelevant',
    'inappropriate',
    'harmful',
    'impersonation',
    'plagiarism',
    'other',
    name='flag_reason'
)

Platform = Enum(
    'Android',
    'iOS',
    'Linux',
    'macOS',
    'Windows',
    name='platform'
)

Notify_Reason = Enum('replied', 'submitted_edit', 'upvoted', name='notify_reason')

Read_Status = Enum('unread', 'read', name='read_status')

class Notification(Base): # pylint: disable=too-few-public-methods
    """Notification model"""
    __tablename__ = 'notification'
    notification_id = Column(
        Integer,
        Identity(start=NOTIFICATION_ID_BASE, cycle=True),
        primary_key=True
    )
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
    created_edit_id = Column(
        Integer,
        ForeignKey('edit.edit_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    created_reply_id = Column(
        Integer,
        ForeignKey('reply.reply_id', onupdate='CASCADE', ondelete='CASCADE')
    )
    notify_reason = Column(Notify_Reason, nullable=False)
    read_status = Column(Read_Status, nullable=False, default='unread')
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
    created_edit = relationship('Edit', foreign_keys=created_edit_id)
    created_reply = relationship('Reply', foreign_keys=created_reply_id)

Follow = Table(
    'follow',
    Base.metadata,
    Column('follower_id', ForeignKey('account.account_id'), primary_key=True),
    Column('following_id', ForeignKey('account.account_id'), primary_key=True)
)

class Account(Base): # pylint: disable=too-few-public-methods
    """Account model"""
    __tablename__ = 'account'
    account_id = Column(Integer, Identity(start=ACCOUNT_ID_BASE, cycle=True), primary_key=True)
    account_role = Column(Account_Role, nullable=False, default='user')
    account_name = Column(String(NAME_LENGTH), unique=True, nullable=False)
    email = Column(String(NAME_LENGTH), unique=True, nullable=False)
    email_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=now())
    edited_at = Column(DateTime, onupdate=now())
    banned_at = Column(DateTime)
    banned_until = Column(DateTime)
    ban_count = Column(Integer, nullable=False, default=0)
    ban_reason = Column(Flag_Reason)
    CheckConstraint(edited_at > created_at)
    photos = relationship('Photo', back_populates='account', cascade='all, delete')
    edits = relationship('Edit', back_populates='account', cascade='all, delete')
    replies = relationship('Reply', back_populates='account', cascade='all, delete')
    upvotes = relationship('Upvote', back_populates='account', cascade='all, delete')
    following = relationship(
        'Account',
        secondary=Follow,
        primaryjoin=account_id == Follow.c.following_id,
        secondaryjoin=account_id == Follow.c.follower_id,
        backref='followers',
        cascade='all, delete',
    )
    notifications = relationship(
        'Notification',
        back_populates='recipient',
        cascade='all, delete',
        primaryjoin=account_id == Notification.recipient_id
    )

class Manufacturer(Base): # pylint: disable=too-few-public-methods
    """Manufacturer model"""
    __tablename__ = 'manufacturer'
    manufacturer_id = Column(
        Integer,
        Identity(start=MANUFACTURER_ID_BASE, cycle=True),
        primary_key=True
    )
    manufacturer_name = Column(String(TITLE_LENGTH), unique=True, nullable=False)
    cameras = relationship('Camera', back_populates='manufacturer')
    lenses = relationship('Lens', back_populates='manufacturer')

class Camera(Base): # pylint: disable=too-few-public-methods
    """Camera model"""
    __tablename__ = 'camera'
    camera_id = Column(Integer, Identity(start=CAMERA_ID_BASE, cycle=True), primary_key=True)
    manufacturer_id = Column(
        Integer,
        ForeignKey('manufacturer.manufacturer_id', onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
    )
    camera_model = Column(String(TITLE_LENGTH), nullable=False)
    UniqueConstraint(camera_model, manufacturer_id)
    manufacturer = relationship('Manufacturer', back_populates='cameras')
    photos = relationship('Photo', back_populates='camera')

class Lens(Base): # pylint: disable=too-few-public-methods
    """Lens model"""
    __tablename__ = 'lens'
    lens_id = Column(Integer, Identity(start=LENS_ID_BASE, cycle=True), primary_key=True)
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

class Editor(Base): # pylint: disable=too-few-public-methods
    """Editor model"""
    __tablename__ = 'editor'
    editor_id = Column(Integer, Identity(start=EDITOR_ID_BASE, cycle=True), primary_key=True)
    editor_name = Column(String(TITLE_LENGTH), nullable=False)
    editor_version = Column(String(20))
    editor_platform = Column(Platform)
    UniqueConstraint(editor_name, editor_version, editor_platform)
    edits = relationship('Edit', back_populates='editor')

class Preview(Base): # pylint: disable=too-few-public-methods
    """Preview model"""
    __tablename__ = 'preview'
    preview_id = Column(Integer, Identity(start=PREVIEW_ID_BASE, cycle=True), primary_key=True)
    preview_file_path = Column(String, unique=True, nullable=False)
    preview_file_size = Column(Integer, nullable=False)
    preview_width = Column(Integer, nullable=False)
    preview_height = Column(Integer, nullable=False)
    CheckConstraint(preview_file_size > 0)
    CheckConstraint(preview_width > 0)
    CheckConstraint(preview_height > 0)

Photo_Tag = Table(
    'photo_tag',
    Base.metadata,
    Column('photo_id', ForeignKey('photo.photo_id'), primary_key=True),
    Column('tag_id', ForeignKey('tag.tag_id'), primary_key=True)
)

class Photo(Base): # pylint: disable=too-few-public-methods
    """Photo model"""
    __tablename__ = 'photo'
    photo_id = Column(Integer, Identity(start=PHOTO_ID_BASE, cycle=True), primary_key=True)
    account_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    preview_id = Column(
        Integer,
        ForeignKey('preview.preview_id', onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
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
    raw_file_extension = Column(String(20), unique=True, nullable=False)
    raw_file_size = Column(Integer, unique=True, nullable=False)
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
    tags = relationship('Tag', secondary=Photo_Tag, back_populates='photos')

class Tag(Base): # pylint: disable=too-few-public-methods
    """Tag model"""
    __tablename__ = 'tag'
    tag_id = Column(Integer, Identity(start=TAG_ID_BASE, cycle=True), primary_key=True)
    tag_name = Column(String(NAME_LENGTH), unique=True, nullable=False)
    photos = relationship('Photo', secondary=Photo_Tag, back_populates='tags')

class Edit(Base): # pylint: disable=too-few-public-methods
    """Edit model"""
    __tablename__ = 'edit'
    edit_id = Column(Integer, Identity(start=EDIT_ID_BASE, cycle=True), primary_key=True)
    account_id = Column(
        Integer,
        ForeignKey('account.account_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    preview_id = Column(
        Integer,
        ForeignKey('preview.preview_id', onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False
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

class Reply(Base): # pylint: disable=too-few-public-methods
    """Reply model"""
    __tablename__ = 'reply'
    reply_id = Column(Integer, Identity(start=REPLY_ID_BASE, cycle=True), primary_key=True)
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

class Upvote(Base): # pylint: disable=too-few-public-methods
    """Upvote model"""
    __tablename__ = 'upvote'
    upvote_id = Column(Integer, Identity(start=UPVOTE_ID_BASE, cycle=True), primary_key=True)
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

class Flag(Base): # pylint: disable=too-few-public-methods
    """Flag model"""
    __tablename__ = 'flag'
    flag_id = Column(Integer, Identity(start=FLAG_ID_BASE, cycle=True), primary_key=True)
    account_id = Column(
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
    flag_reason = Column(Flag_Reason, nullable=False)
    reason_text = Column(String(SHORT_TEXT))
    created_at = Column(DateTime, nullable=False, default=now())
    UniqueConstraint(
        account_id,
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
    account = relationship('Account', foreign_keys=account_id)
    flagged_account = relationship('Account', foreign_keys=flagged_account_id)
    flagged_photo = relationship('Photo', foreign_keys=flagged_photo_id)
    flagged_edit = relationship('Edit', foreign_keys=flagged_edit_id)
    flagged_reply = relationship('Reply', foreign_keys=flagged_reply_id)
