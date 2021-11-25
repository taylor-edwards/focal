"""Graphene schema for GraphQL support"""

from datetime import datetime
from graphene import Argument, DateTime, Field, ID, Int, List, ObjectType, Schema, String
from graphene_sqlalchemy import SQLAlchemyObjectType
from model import (
    Notification as NotificationModel,
    Account as AccountModel,
    Manufacturer as ManufacturerModel,
    Camera as CameraModel,
    Lens as LensModel,
    Editor as EditorModel,
    Preview as PreviewModel,
    Photo as PhotoModel,
    Tag as TagModel,
    Edit as EditModel,
    Reply as ReplyModel,
    Upvote as UpvoteModel,
    Flag as FlagModel,
    Ban as BanModel
)

class Notification(SQLAlchemyObjectType):
    """Notification object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = NotificationModel

class Account(SQLAlchemyObjectType):
    """Account object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = AccountModel

class Ban(SQLAlchemyObjectType):
    """Ban object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = BanModel

class Manufacturer(SQLAlchemyObjectType):
    """Manufacturer object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = ManufacturerModel

class Camera(SQLAlchemyObjectType):
    """Camera object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = CameraModel

class Lens(SQLAlchemyObjectType):
    """Lens object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = LensModel

class Editor(SQLAlchemyObjectType):
    """Editor object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = EditorModel

class Preview(SQLAlchemyObjectType):
    """Preview object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = PreviewModel

class Photo(SQLAlchemyObjectType):
    """Photo object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = PhotoModel

class Tag(SQLAlchemyObjectType):
    """Tag object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = TagModel

class Edit(SQLAlchemyObjectType):
    """Edit object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = EditModel

class Reply(SQLAlchemyObjectType):
    """Reply object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = ReplyModel

class Upvote(SQLAlchemyObjectType):
    """Upvote object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = UpvoteModel

class Flag(SQLAlchemyObjectType):
    """Flag object type"""
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-class-docstring,too-few-public-methods
        model = FlagModel

class Query(ObjectType):
    """Wrapper for all queries"""
    # pylint: disable=too-many-public-methods
    account = Field(Account, account_id=Argument(type=ID), account_name=Argument(type=String))
    def resolve_account(self, info, account_id=None, account_name=None):
        """Query for account by ID"""
        # pylint: disable=no-self-use
        if account_id is not None:
            return Account.get_query(info=info) \
                          .filter(AccountModel.account_id == account_id) \
                          .first()
        if account_name is not None:
            return Account.get_query(info=info) \
                          .filter(AccountModel.account_name == account_name) \
                          .first()
        return None

    accounts = List(Account, limit=Argument(type=Int), offset=Argument(type=Int), \
                    before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_accounts(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all accounts"""
         # pylint: disable=no-self-use
        return Account.get_query(info)
                      .filter(AccountModel.edited_at <= before) \
                      .filter(AccountModel.edited_at > after) \
                      .order_by(AccountModel.edited_at, AccountModel.created_at) \
                      .limit(limit) \
                      .offset(offset)

    notification = Field(Notification, notification_id=Argument(type=ID, required=True))
    def resolve_notification(self, info, notification_id=None):
        """Query for notification by ID"""
         # pylint: disable=no-self-use
        return Notification.get_query(info=info) \
                           .filter(NotificationModel.notification_id == notification_id) \
                           .first()

    flag = Field(Flag, flag_id=Argument(type=ID, required=True))
    def resolve_flag(self, info, flag_id=None):
        """Query for flag by ID"""
         # pylint: disable=no-self-use
        return Flag.get_query(info=info).filter(FlagModel.flag_id == flag_id).first()

    flags = List(Flag, limit=Argument(type=Int), offset=Argument(type=Int), \
                 before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_flags(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all flags"""
         # pylint: disable=no-self-use
        return Flag.get_query(info)
                   .filter(FlagModel.edited_at <= before) \
                   .filter(FlagModel.edited_at > after) \
                   .order_by(FlagModel.edited_at, FlagModel.created_at) \
                   .limit(limit) \
                   .offset(offset)

    ban = Field(Ban, ban_id=Argument(type=ID, required=True))
    def resolve_ban(self, info, ban_id):
        """Query for ban by ID"""
        # pylint: disable=no-self-use
        return Ban.get_query(info=info).filter(BanModel.ban_id == ban_id).first()

    bans = List(Ban, limit=Argument(type=Int), offset=Argument(type=Int), \
                before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_bans(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all bans"""
         # pylint: disable=no-self-use
        return Ban.get_query(info)
                  .filter(BanModel.edited_at <= before) \
                  .filter(BanModel.edited_at > after) \
                  .order_by(BanModel.edited_at, BanModel.created_at) \
                  .limit(limit) \
                  .offset(offset)

    camera = Field(Camera, camera_id=Argument(type=ID, required=True))
    def resolve_camera(self, info, camera_id=None):
        """Query for camera by ID"""
         # pylint: disable=no-self-use
        return Camera.get_query(info=info).filter(CameraModel.camera_id == camera_id).first()

    cameras = List(Camera, limit=Argument(type=Int), offset=Argument(type=Int), \
                   before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_cameras(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all cameras"""
         # pylint: disable=no-self-use
        return Camera.get_query(info)
                     .filter(CameraModel.edited_at <= before) \
                     .filter(CameraModel.edited_at > after) \
                     .order_by(CameraModel.edited_at, CameraModel.created_at) \
                     .limit(limit) \
                     .offset(offset)

    edit = Field(Edit, edit_id=Argument(type=ID, required=True))
    def resolve_edit(self, info, edit_id=None):
        """Query for edit by ID"""
         # pylint: disable=no-self-use
        return Edit.get_query(info=info).filter(EditModel.edit_id == edit_id).first()

    edits = List(Edit, limit=Argument(type=Int), offset=Argument(type=Int), \
                 before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_edits(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all edits"""
         # pylint: disable=no-self-use
        return Edit.get_query(info)
                   .filter(EditModel.edited_at <= before) \
                   .filter(EditModel.edited_at > after) \
                   .order_by(EditModel.edited_at, EditModel.created_at) \
                   .limit(limit) \
                   .offset(offset)

    editor = Field(Editor, editor_id=Argument(type=ID, required=True))
    def resolve_editor(self, info, editor_id=None):
        """Query for editor by ID"""
         # pylint: disable=no-self-use
        return Editor.get_query(info=info).filter(EditorModel.editor_id == editor_id).first()

    editors = List(Editor, limit=Argument(type=Int), offset=Argument(type=Int), \
                   before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_editors(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all editors"""
         # pylint: disable=no-self-use
        return Editor.get_query(info)
                     .filter(EditorModel.edited_at <= before) \
                     .filter(EditorModel.edited_at > after) \
                     .order_by(EditorModel.edited_at, EditorModel.created_at) \
                     .limit(limit) \
                     .offset(offset)

    lens = Field(Lens, lens_id=Argument(type=ID, required=True))
    def resolve_lens(self, info, lens_id=None):
        """Query for lens by ID"""
         # pylint: disable=no-self-use
        return Lens.get_query(info=info).filter(LensModel.lens_id == lens_id).first()

    lenses = List(Lens, limit=Argument(type=Int), offset=Argument(type=Int), \
                  before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_lenses(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all lenses"""
         # pylint: disable=no-self-use
        return Lens.get_query(info)
                   .filter(LensModel.edited_at <= before) \
                   .filter(LensModel.edited_at > after) \
                   .order_by(LensModel.edited_at, LensModel.created_at) \
                   .limit(limit) \
                   .offset(offset)

    manufacturer = Field(Manufacturer, manufacturer_id=Argument(type=ID, required=True))
    def resolve_manufacturer(self, info, manufacturer_id=None):
        """Query for manufacturer by ID"""
         # pylint: disable=no-self-use
        return Manufacturer.get_query(info=info) \
                           .filter(ManufacturerModel.manufacturer_id == manufacturer_id) \
                           .first()

    manufacturers = List(Manufacturer, limit=Argument(type=Int), offset=Argument(type=Int), \
                         before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_manufacturers(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all manufacturers"""
         # pylint: disable=no-self-use
        return Manufacturer.get_query(info)
                           .filter(ManufacturerModel.edited_at <= before) \
                           .filter(ManufacturerModel.edited_at > after) \
                           .order_by(ManufacturerModel.edited_at, ManufacturerModel.created_at) \
                           .limit(limit) \
                           .offset(offset)

    photo = Field(Photo, photo_id=Argument(type=ID, required=True))
    def resolve_photo(self, info, photo_id=None):
        """Query for photo by ID"""
         # pylint: disable=no-self-use
        return Photo.get_query(info=info).filter(PhotoModel.photo_id == photo_id).first()

    photos = List(Photo, limit=Argument(type=Int), offset=Argument(type=Int), \
                  before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_photos(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all photos"""
         # pylint: disable=no-self-use
        return Photo.get_query(info)
                    .filter(PhotoModel.edited_at <= before) \
                    .filter(PhotoModel.edited_at > after) \
                    .order_by(PhotoModel.edited_at, PhotoModel.created_at) \
                    .limit(limit) \
                    .offset(offset)

    preview = Field(Preview, preview_id=Argument(type=ID, required=True))
    def resolve_preview(self, info, preview_id=None):
        """Query for preview by ID"""
         # pylint: disable=no-self-use
        return Preview.get_query(info=info).filter(PreviewModel.preview_id == preview_id).first()

    previews = List(Preview, limit=Argument(type=Int), offset=Argument(type=Int), \
                    before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_previews(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all previews"""
         # pylint: disable=no-self-use
        return Preview.get_query(info=info).filter(PreviewModel.edited_at <= before) \
                      .filter(PreviewModel.edited_at > after) \
                      .order_by(PreviewModel.edited_at, PreviewModel.created_at) \
                      .limit(limit) \
                      .offset(offset)

    reply = Field(Reply, reply_id=Argument(type=ID, required=True))
    def resolve_reply(self, info, reply_id=None):
        """Query for reply by ID"""
         # pylint: disable=no-self-use
        return Reply.get_query(info=info).filter(ReplyModel.reply_id == reply_id).first()

    tag = Field(Tag, tag_id=Argument(type=ID, required=True))
    def resolve_tag(self, info, tag_id=None):
        """Query for tag by ID"""
         # pylint: disable=no-self-use
        return Tag.get_query(info=info).filter(TagModel.tag_id == tag_id).first()

    tags = List(Tag, limit=Argument(type=Int), offset=Argument(type=Int), \
                before=Argument(type=DateTime), after=Argument(type=DateTime))
    def resolve_tags(self, info, limit=10, offset=0, before=datetime.max, after=datetime.min):
        """Query for all tags"""
         # pylint: disable=no-self-use
        return Tag.get_query(info)
                  .filter(TagModel.edited_at <= before) \
                  .filter(TagModel.edited_at > after) \
                  .order_by(TagModel.edited_at, TagModel.created_at) \
                  .limit(limit) \
                  .offset(offset)

    upvote = Field(Upvote, upvote_id=Argument(type=ID, required=True))
    def resolve_upvote(self, info, upvote_id=None):
        """Query for upvote by ID"""
         # pylint: disable=no-self-use
        return Upvote.get_query(info=info).filter(UpvoteModel.upvote_id == upvote_id).first()


schema = Schema(query=Query)
