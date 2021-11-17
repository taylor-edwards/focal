"""Graphene schema for GraphQL support"""

from graphene import Argument, Field, ID, List, ObjectType, Schema
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
    Flag as FlagModel
)

class Notification(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Notification type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = NotificationModel

class Account(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Account type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = AccountModel

class Manufacturer(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Manufacturer type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = ManufacturerModel

class Camera(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Camera type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = CameraModel

class Lens(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Lens type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = LensModel

class Editor(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Editor type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = EditorModel

class Preview(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Preview type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = PreviewModel

class Photo(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Photo type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = PhotoModel

class Tag(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Tag type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = TagModel

class Edit(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Edit type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = EditModel

class Reply(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Reply type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = ReplyModel

class Upvote(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Upvote type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = UpvoteModel

class Flag(SQLAlchemyObjectType): # pylint: disable=too-few-public-methods
    """Flag type for GraphQL"""
    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        model = FlagModel

class Query(ObjectType): # pylint: disable=too-few-public-methods
    """Queries for GraphQL"""
    account = Field(Account, account_id=Argument(type=ID, required=True))
    def resolve_account(self, info, account_id=None): # pylint: disable=no-self-use
        """Query for account by ID"""
        return Account.get_query(info=info) \
                      .filter(AccountModel.account_id == account_id) \
                      .first()

    accounts = List(Account)
    def resolve_accounts(self, info): # pylint: disable=no-self-use
        """Query for all accounts"""
        return Account.get_query(info).all()

    camera = Field(Camera, camera_id=Argument(type=ID, required=True))
    def resolve_camera(self, info, camera_id=None): # pylint: disable=no-self-use
        """Query for camera by ID"""
        return Camera.get_query(info=info) \
                     .filter(CameraModel.camera_id == camera_id) \
                     .first()

    cameras = List(Camera)
    def resolve_cameras(self, info): # pylint: disable=no-self-use
        """Query for all cameras"""
        return Camera.get_query(info).all()

    edit = Field(Edit, edit_id=Argument(type=ID, required=True))
    def resolve_edit(self, info, edit_id=None): # pylint: disable=no-self-use
        """Query for edit by ID"""
        return Edit.get_query(info=info) \
                   .filter(EditModel.edit_id == edit_id) \
                   .first()

    edits = List(Edit)
    def resolve_edits(self, info): # pylint: disable=no-self-use
        """Query for all edits"""
        return Edit.get_query(info).all()

    editor = Field(Editor, editor_id=Argument(type=ID, required=True))
    def resolve_editor(self, info, editor_id=None): # pylint: disable=no-self-use
        """Query for editor by ID"""
        return Editor.get_query(info=info) \
                     .filter(EditorModel.editor_id == editor_id) \
                     .first()

    editors = List(Editor)
    def resolve_editors(self, info): # pylint: disable=no-self-use
        """Query for all editors"""
        return Editor.get_query(info).all()

    flag = Field(Flag, flag_id=Argument(type=ID, required=True))
    def resolve_flag(self, info, flag_id=None): # pylint: disable=no-self-use
        """Query for flag by ID"""
        return Flag.get_query(info=info) \
                   .filter(FlagModel.flag_id == flag_id) \
                   .first()

    lens = Field(Lens, lens_id=Argument(type=ID, required=True))
    def resolve_lens(self, info, lens_id=None): # pylint: disable=no-self-use
        """Query for lens by ID"""
        return Lens.get_query(info=info) \
                   .filter(LensModel.lens_id == lens_id) \
                   .first()

    lenses = List(Lens)
    def resolve_lenses(self, info): # pylint: disable=no-self-use
        """Query for all lenses"""
        return Lens.get_query(info).all()

    manufacturer = Field(Manufacturer, manufacturer_id=Argument(type=ID, required=True))
    def resolve_manufacturer(self, info, manufacturer_id=None): # pylint: disable=no-self-use
        """Query for manufacturer by ID"""
        return Manufacturer.get_query(info=info) \
                           .filter(ManufacturerModel.manufacturer_id == manufacturer_id) \
                           .first()

    manufacturers = List(Manufacturer)
    def resolve_manufacturers(self, info): # pylint: disable=no-self-use
        """Query for all manufacturers"""
        return Manufacturer.get_query(info).all()

    notification = Field(Notification, notification_id=Argument(type=ID, required=True))
    def resolve_notification(self, info, notification_id=None): # pylint: disable=no-self-use
        """Query for notification by ID"""
        return Notification.get_query(info=info) \
                           .filter(NotificationModel.notification_id == notification_id) \
                           .first()

    photo = Field(Photo, photo_id=Argument(type=ID, required=True))
    def resolve_photo(self, info, photo_id=None): # pylint: disable=no-self-use
        """Query for photo by ID"""
        return Photo.get_query(info=info) \
                    .filter(PhotoModel.photo_id == photo_id) \
                    .first()

    photos = List(Photo)
    def resolve_photos(self, info): # pylint: disable=no-self-use
        """Query for all photos"""
        return Photo.get_query(info).all()

    preview = Field(Preview, preview_id=Argument(type=ID, required=True))
    def resolve_preview(self, info, preview_id=None): # pylint: disable=no-self-use
        """Query for preview by ID"""
        return Preview.get_query(info=info) \
                      .filter(PreviewModel.preview_id == preview_id) \
                      .first()

    reply = Field(Reply, reply_id=Argument(type=ID, required=True))
    def resolve_reply(self, info, reply_id=None): # pylint: disable=no-self-use
        """Query for reply by ID"""
        return Reply.get_query(info=info) \
                    .filter(ReplyModel.reply_id == reply_id) \
                    .first()

    tag = Field(Tag, tag_id=Argument(type=ID, required=True))
    def resolve_tag(self, info, tag_id=None): # pylint: disable=no-self-use
        """Query for tag by ID"""
        return Tag.get_query(info=info) \
                  .filter(TagModel.tag_id == tag_id) \
                  .first()

    tags = List(Tag)
    def resolve_tags(self, info): # pylint: disable=no-self-use
        """Query for all tags"""
        return Tag.get_query(info).all()

    upvote = Field(Upvote, upvote_id=Argument(type=ID, required=True))
    def resolve_upvote(self, info, upvote_id=None): # pylint: disable=no-self-use
        """Query for upvote by ID"""
        return Upvote.get_query(info=info) \
                     .filter(UpvoteModel.upvote_id == upvote_id) \
                     .first()

schema = Schema(query=Query)
