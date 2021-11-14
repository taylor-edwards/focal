"""Graphene schema for GraphQL support"""

from graphene import Argument, Field, ID, ObjectType, Schema
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
    camera = Field(Camera, camera_id=Argument(type=ID, required=True))
    edit = Field(Edit, edit_id=Argument(type=ID, required=True))
    editor = Field(Editor, editor_id=Argument(type=ID, required=True))
    flag = Field(Flag, flag_id=Argument(type=ID, required=True))
    lens = Field(Lens, lens_id=Argument(type=ID, required=True))
    manufacturer = Field(Manufacturer, manufacturer_id=Argument(type=ID, required=True))
    notification = Field(Notification, notification_id=Argument(type=ID, required=True))
    photo = Field(Photo, photo_id=Argument(type=ID, required=True))
    preview = Field(Preview, preview_id=Argument(type=ID, required=True))
    reply = Field(Reply, reply_id=Argument(type=ID, required=True))
    tag = Field(Tag, tag_id=Argument(type=ID, required=True))
    upvote = Field(Upvote, upvote_id=Argument(type=ID, required=True))

    def resolve_account(self, info, account_id=None): # pylint: disable=no-self-use
        """Retrieve account by ID"""
        query = Account.get_query(info=info)
        if account_id:
            query = query.filter(AccountModel.account_id == account_id)
        return query.first()

    def resolve_camera(self, info, camera_id=None): # pylint: disable=no-self-use
        """Retrieve camera by ID"""
        query = Camera.get_query(info=info)
        if camera_id:
            query = query.filter(CameraModel.camera_id == camera_id)
        return query.first()

    def resolve_edit(self, info, edit_id=None): # pylint: disable=no-self-use
        """Retrieve edit by ID"""
        query = Edit.get_query(info=info)
        if edit_id:
            query = query.filter(EditModel.edit_id == edit_id)
        return query.first()

    def resolve_editor(self, info, editor_id=None): # pylint: disable=no-self-use
        """Retrieve editor by ID"""
        query = Editor.get_query(info=info)
        if editor_id:
            query = query.filter(EditorModel.editor_id == editor_id)
        return query.first()

    def resolve_flag(self, info, flag_id=None): # pylint: disable=no-self-use
        """Retrieve flag by ID"""
        query = Flag.get_query(info=info)
        if flag_id:
            query = query.filter(FlagModel.flag_id == flag_id)
        return query.first()

    def resolve_lens(self, info, lens_id=None): # pylint: disable=no-self-use
        """Retrieve lens by ID"""
        query = Lens.get_query(info=info)
        if lens_id:
            query = query.filter(LensModel.lens_id == lens_id)
        return query.first()

    def resolve_manufacturer(self, info, manufacturer_id=None): # pylint: disable=no-self-use
        """Retrieve manufacturer by ID"""
        query = Manufacturer.get_query(info=info)
        if manufacturer_id:
            query = query.filter(ManufacturerModel.manufacturer_id == manufacturer_id)
        return query.first()

    def resolve_notification(self, info, notification_id=None): # pylint: disable=no-self-use
        """Retrieve notification by ID"""
        query = Notification.get_query(info=info)
        if notification_id:
            query = query.filter(NotificationModel.notification_id == notification_id)
        return query.first()

    def resolve_photo(self, info, photo_id=None): # pylint: disable=no-self-use
        """Retrieve photo by ID"""
        query = Photo.get_query(info=info)
        if photo_id:
            query = query.filter(PhotoModel.photo_id == photo_id)
        return query.first()

    def resolve_preview(self, info, preview_id=None): # pylint: disable=no-self-use
        """Retrieve preview by ID"""
        query = Preview.get_query(info=info)
        if preview_id:
            query = query.filter(PreviewModel.preview_id == preview_id)
        return query.first()

    def resolve_reply(self, info, reply_id=None): # pylint: disable=no-self-use
        """Retrieve reply by ID"""
        query = Reply.get_query(info=info)
        if reply_id:
            query = query.filter(ReplyModel.reply_id == reply_id)
        return query.first()

    def resolve_tag(self, info, tag_id=None): # pylint: disable=no-self-use
        """Retrieve tag by ID"""
        query = Tag.get_query(info=info)
        if tag_id:
            query = query.filter(TagModel.tag_id == tag_id)
        return query.first()

    def resolve_upvote(self, info, upvote_id=None): # pylint: disable=no-self-use
        """Retrieve upvote by ID"""
        query = Upvote.get_query(info=info)
        if upvote_id:
            query = query.filter(UpvoteModel.upvote_id == upvote_id)
        return query.first()

schema = Schema(query=Query)
