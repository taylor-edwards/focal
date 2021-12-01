"""Graphene schema for GraphQL support"""
# pylint: disable=too-few-public-methods,too-many-arguments,no-self-use,missing-class-docstring

from datetime import datetime
from graphene import Argument, DateTime, Field, ID, Int, List, ObjectType, Schema, String
from graphene_sqlalchemy import SQLAlchemyObjectType
from model import (
    Account as AccountModel,
    Photo as PhotoModel,
    Edit as EditModel,
    Reply as ReplyModel,
    Reaction as ReactionModel,
    File as FileModel,
    Tag as TagModel,
    Manufacturer as ManufacturerModel,
    Camera as CameraModel,
    Lens as LensModel,
    Editor as EditorModel,
    Event as EventModel,
    Notification as NotificationModel,
    Flag as FlagModel,
    Ban as BanModel
)

class Account(SQLAlchemyObjectType):
    class Meta:
        model = AccountModel

class Photo(SQLAlchemyObjectType):
    class Meta:
        model = PhotoModel

class Edit(SQLAlchemyObjectType):
    class Meta:
        model = EditModel

class Reply(SQLAlchemyObjectType):
    class Meta:
        model = ReplyModel

class Reaction(SQLAlchemyObjectType):
    class Meta:
        model = ReactionModel

class File(SQLAlchemyObjectType):
    class Meta:
        model = FileModel

class Tag(SQLAlchemyObjectType):
    class Meta:
        model = TagModel

class Manufacturer(SQLAlchemyObjectType):
    class Meta:
        model = ManufacturerModel

class Camera(SQLAlchemyObjectType):
    class Meta:
        model = CameraModel

class Lens(SQLAlchemyObjectType):
    class Meta:
        model = LensModel

class Editor(SQLAlchemyObjectType):
    class Meta:
        model = EditorModel

class Event(SQLAlchemyObjectType):
    class Meta:
        model = EventModel

class Notification(SQLAlchemyObjectType):
    class Meta:
        model = NotificationModel

class Flag(SQLAlchemyObjectType):
    class Meta:
        model = FlagModel

class Ban(SQLAlchemyObjectType):
    class Meta:
        model = BanModel

class Query(ObjectType):
    """Query resolvers"""
    # pylint: disable=too-many-public-methods
    account = Field(Account, account_name=Argument(type=String))
    def resolve_account(self, info, account_name=None):
        """Query for account by public name"""
        if account_name is not None:
            return Account.get_query(info) \
                          .filter(AccountModel.account_name == account_name) \
                          .first()
        return None

    accounts = List(Account, limit=Argument(type=Int), offset=Argument(type=Int),
                    before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_accounts(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all accounts"""
        return Account.get_query(info) \
                      .filter(AccountModel.edited_at < before) \
                      .filter(AccountModel.edited_at >= after) \
                      .order_by(AccountModel.edited_at.desc(), AccountModel.created_at.desc()) \
                      .limit(limit) \
                      .offset(offset)

    photo = Field(Photo, photo_id=Argument(type=ID, required=True))
    def resolve_photo(self, info, photo_id=None):
        """Query for photo by ID"""
        return Photo.get_query(info).filter(PhotoModel.photo_id == photo_id).first()

    photos = List(Photo, limit=Argument(type=Int), offset=Argument(type=Int),
                  before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_photos(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all photos"""
        return Photo.get_query(info) \
                    .filter(PhotoModel.edited_at < before) \
                    .filter(PhotoModel.edited_at >= after) \
                    .order_by(PhotoModel.edited_at.desc(), PhotoModel.created_at.desc()) \
                    .limit(limit) \
                    .offset(offset)

    edit = Field(Edit, edit_id=Argument(type=ID, required=True))
    def resolve_edit(self, info, edit_id=None):
        """Query for edit by ID"""
        return Edit.get_query(info).filter(EditModel.edit_id == edit_id).first()

    edits = List(Edit, limit=Argument(type=Int), offset=Argument(type=Int),
                 before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_edits(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all edits"""
        return Edit.get_query(info) \
                   .filter(EditModel.edited_at < before) \
                   .filter(EditModel.edited_at >= after) \
                   .order_by(EditModel.edited_at.desc(), EditModel.created_at.desc()) \
                   .limit(limit) \
                   .offset(offset)

    reply = Field(Reply, reply_id=Argument(type=ID, required=True))
    def resolve_reply(self, info, reply_id=None):
        """Query for reply by ID"""
        return Reply.get_query(info).filter(ReplyModel.reply_id == reply_id).first()

    replies = List(Reply, limit=Argument(type=Int), offset=Argument(type=Int),
                   before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_replies(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all replies by date"""
        return Reply.get_query(info) \
                    .filter(ReplyModel.edited_at < before) \
                    .filter(ReplyModel.edited_at >= after) \
                    .order_by(ReplyModel.edited_at.desc(), ReplyModel.created_at.desc()) \
                    .limit(limit) \
                    .offset(offset)

    reaction = Field(Reaction, reaction_id=Argument(type=ID, required=True))
    def resolve_reaction(self, info, reaction_id=None):
        """Query for reaction by ID"""
        return Reaction.get_query(info).filter(ReactionModel.reaction_id == reaction_id).first()

    reactions = List(Reaction, limit=Argument(type=Int), offset=Argument(type=Int))
    def resolve_reactions(self, info, limit=10, offset=0):
        """Query for all reactions by date"""
        return Reaction.get_query(info).limit(limit).offset(offset)

    tag = Field(Tag, tag_id=Argument(type=ID, required=True))
    def resolve_tag(self, info, tag_id=None):
        """Query for tag by ID"""
        return Tag.get_query(info).filter(TagModel.tag_id == tag_id).first()

    tags = List(Tag, limit=Argument(type=Int), offset=Argument(type=Int))
    def resolve_tags(self, info, limit=10, offset=0):
        """Query for all tags"""
        return Tag.get_query(info).limit(limit).offset(offset)

    manufacturer = Field(Manufacturer, manufacturer_id=Argument(type=ID, required=True))
    def resolve_manufacturer(self, info, manufacturer_id=None):
        """Query for manufacturer by ID"""
        return Manufacturer.get_query(info) \
                           .filter(ManufacturerModel.manufacturer_id == manufacturer_id) \
                           .first()

    manufacturers = List(Manufacturer, limit=Argument(type=Int), offset=Argument(type=Int))
    def resolve_manufacturers(self, info, limit=10, offset=0):
        """Query for all manufacturers"""
        return Manufacturer.get_query(info) \
                           .order_by(ManufacturerModel.manufacturer_name) \
                           .limit(limit) \
                           .offset(offset)

    camera = Field(Camera, camera_id=Argument(type=ID, required=True))
    def resolve_camera(self, info, camera_id=None):
        """Query for camera by ID"""
        return Camera.get_query(info).filter(CameraModel.camera_id == camera_id).first()

    cameras = List(Camera, limit=Argument(type=Int), offset=Argument(type=Int))
    def resolve_cameras(self, info, limit=10, offset=0):
        """Query for all cameras"""
        return Camera.get_query(info) \
                     .order_by(CameraModel.camera_model) \
                     .limit(limit) \
                     .offset(offset)

    lens = Field(Lens, lens_id=Argument(type=ID, required=True))
    def resolve_lens(self, info, lens_id=None):
        """Query for lens by ID"""
        return Lens.get_query(info).filter(LensModel.lens_id == lens_id).first()

    lenses = List(Lens, limit=Argument(type=Int), offset=Argument(type=Int))
    def resolve_lenses(self, info, limit=10, offset=0):
        """Query for all lenses"""
        return Lens.get_query(info) \
                   .order_by(LensModel.lens_model) \
                   .limit(limit) \
                   .offset(offset)

    editor = Field(Editor, editor_id=Argument(type=ID, required=True))
    def resolve_editor(self, info, editor_id=None):
        """Query for editor by ID"""
        return Editor.get_query(info).filter(EditorModel.editor_id == editor_id).first()

    editors = List(Editor, limit=Argument(type=Int), offset=Argument(type=Int))
    def resolve_editors(self, info, limit=10, offset=0):
        """Query for all editors"""
        return Editor.get_query(info) \
                     .order_by(EditorModel.editor_name) \
                     .limit(limit) \
                     .offset(offset)

    file = Field(File, file_id=Argument(type=ID, required=True))
    def resolve_file(self, info, file_id=None):
        """Query for file by ID"""
        return File.get_query(info).filter(FileModel.file_id == file_id).first()

    files = List(File, limit=Argument(Int), offset=Argument(Int),
                 before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_files(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all files"""
        return File.get_query(info) \
                   .filter(FileModel.created_at < before) \
                   .filter(FileModel.created_at >= after) \
                   .order_by(FileModel.created_at.desc()) \
                   .limit(limit) \
                   .offset(offset)

    event = Field(Event, event_id=Argument(type=ID, required=True))
    def resolve_event(self, info, event_id=None):
        if event_id is not None:
            return Event.get_query(info).filter(EventModel.event_id == event_id).first()
        return None

    events = List(Event, limit=Argument(type=Int), offset=Argument(type=Int),
                  before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_events(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all event items"""
        return Event.get_query(info) \
                    .filter(EventModel.created_at < before) \
                    .filter(EventModel.created_at >= after) \
                    .order_by(EventModel.created_at.desc()) \
                    .limit(limit) \
                    .offset(offset)

    notification = Field(Notification, notification_id=Argument(type=ID, required=True))
    def resolve_notification(self, info, notification_id=None):
        """Query for notification by ID"""
        return Notification.get_query(info) \
                           .filter(NotificationModel.notification_id == notification_id) \
                           .first()

    notifications = List(Notification, limit=Argument(type=Int), offset=Argument(type=Int),
                         before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_notifications(self, info, limit=10, offset=0,
                              before=datetime.max, after=datetime.min):
        """Query for all notifications"""
        return Notification.get_query(info) \
                           .filter(NotificationModel.created_at < before) \
                           .filter(NotificationModel.created_at >= after) \
                           .order_by(NotificationModel.created_at.desc()) \
                           .limit(limit) \
                           .offset(offset)

    flag = Field(Flag, flag_id=Argument(type=ID, required=True))
    def resolve_flag(self, info, flag_id=None):
        """Query for flag by ID"""
        return Flag.get_query(info).filter(FlagModel.flag_id == flag_id).first()

    flags = List(Flag, limit=Argument(type=Int), offset=Argument(type=Int),
                 before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_flags(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all flags"""
        return Flag.get_query(info) \
                   .filter(FlagModel.created_at < before) \
                   .filter(FlagModel.created_at >= after) \
                   .order_by(FlagModel.created_at.desc()) \
                   .limit(limit) \
                   .offset(offset)

    ban = Field(Ban, ban_id=Argument(type=ID, required=True))
    def resolve_ban(self, info, ban_id):
        """Query for ban by ID"""
        return Ban.get_query(info).filter(BanModel.ban_id == ban_id).first()

    bans = List(Ban, limit=Argument(type=Int), offset=Argument(type=Int),
                before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_bans(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all bans"""
        return Ban.get_query(info) \
                  .filter(BanModel.created_at < before) \
                  .filter(BanModel.created_at >= after) \
                  .order_by(BanModel.created_at.desc()) \
                  .limit(limit) \
                  .offset(offset)

schema = Schema(query=Query)
