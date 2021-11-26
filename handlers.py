"""Database interface"""

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now
from model import (
    Account,
    Camera,
    Edit,
    Editor,
    Lens,
    Manufacturer,
    Photo,
    Preview,
    Reply,
    Tag,
    Reaction
)

def select_account(engine, account_id=None, account_email=None, account_name=None):
    """Select an account by ID"""
    with Session(engine) as session:
        if account_id is not None:
            return session.query(Account).filter_by(account_id=account_id).first()
        if account_email is not None:
            return session.query(Account).filter_by(account_email=account_email).first()
        if account_name is not None:
            return session.query(Account).filter_by(account_name=account_name).first()
        return None

def create_account(engine, account_name, account_email, account_role='user'):
    """Create an account"""
    with Session(engine) as session:
        account = session.query(Account).filter_by(account_email=account_email).first()
        if account is not None:
            raise Exception(f'Account email in use ({account_email})')

        account = session.query(Account).filter_by(account_name=account_name).first()
        if account is not None:
            raise Exception(f'Account name in use ({account_name})')

        if account_role not in ('user', 'admin'):
            raise Exception('Account role does not exist')

        account = Account(
            account_name=account_name,
            account_email=account_email,
            account_role=account_role
        )
        session.add(account)
        session.commit()
        session.refresh(account)
        return account

def update_account(
    engine,
    account_id,
    account_name=None,
    account_role=None,
    account_email=None,
    is_verified=None
):
    """Update an account"""
    # pylint: disable=too-many-arguments
    with Session(engine) as session:
        account_updates = {}
        if account_name is not None:
            account = session.query(Account).filter_by(account_name=account_name).first()
            if account is not None:
                raise Exception(f'Account name in use ({account_name})')
            account_updates['account_name'] = account_name

        if account_email is not None:
            account = session.query(Account).filter_by(account_email=account_email).first()
            if account is not None:
                raise Exception(f'Account email in use ({account_email})')
            account_updates['account_email'] = account_email

        if account_role is not None:
            if account_role not in ('user', 'admin'):
                raise Exception('Account role does not exist')
            account_updates['account_role'] = account_role

        if is_verified is not None:
            account_updates['verified_at'] = now() if is_verified else None

        session.query(Account).filter_by(account_id=account_id).update(account_updates)
        session.commit()

def delete_account(engine, account_id):
    """Delete an account"""
    with Session(engine) as session:
        account = select_account(engine, account_id=account_id)
        if account is not None:
            session.delete(account)
            session.commit()
        else:
            raise Exception('Account not found')

def select_photo(engine, photo_id=None, account_id=None, photo_title=None, preview_id=None):
    """Select a photo"""
    with Session(engine) as session:
        if photo_id is not None:
            return session.query(Photo).filter_by(photo_id=photo_id).first()
        if account_id is not None and photo_title is not None:
            return session.query(Photo) \
                          .filter_by(account_id=account_id, photo_title=photo_title) \
                          .first()
        if preview_id is not None:
            return session.query(Photo) \
                          .filter_by(preview_id=preview_id) \
                          .first()
        return None

def create_photo(
    engine,
    account_id,
    photo_title,
    preview_id=None,
    camera_id=None,
    lens_id=None,
    photo_description=None,
    raw_file_name=None,
    raw_file_path=None,
    raw_file_extension=None,
    raw_file_size=None,
    raw_width=None,
    raw_height=None,
    aperture=None,
    flash=None,
    focal_length=None,
    iso=None,
    shutter_speed_denominator=None,
    shutter_speed_numerator=None
):
    """Create a photo"""
    # pylint: disable=too-many-arguments,too-many-locals
    with Session(engine) as session:
        photo = select_photo(engine, account_id=account_id, photo_title=photo_title)
        if photo is not None:
            raise Exception(f'Photo title in use by account ({photo_title}, {account_id})')
        photo = Photo(
            account_id=account_id,
            photo_title=photo_title,
            preview_id=preview_id,
            camera_id=camera_id,
            lens_id=lens_id,
            photo_description=photo_description,
            raw_file_name=raw_file_name,
            raw_file_path=raw_file_path,
            raw_file_extension=raw_file_extension,
            raw_file_size=raw_file_size,
            raw_width=raw_width,
            raw_height=raw_height,
            aperture=aperture,
            flash=flash,
            focal_length=focal_length,
            iso=iso,
            shutter_speed_denominator=shutter_speed_denominator,
            shutter_speed_numerator=shutter_speed_numerator
        )
        session.add(photo)
        session.commit()
        session.refresh(photo)
        return photo

def update_photo(
    engine,
    photo_id,
    **property_overrides
):
    """Update a photo"""
    photo_property_list = [
        'account_id',
        'preview_id',
        'camera_id',
        'lens_id',
        'photo_title',
        'photo_description',
        'raw_file_path',
        'raw_file_extension',
        'raw_file_size',
        'raw_width',
        'raw_height',
        'aperture',
        'flash',
        'focal_length',
        'iso',
        'shutter_speed_denominator',
        'shutter_speed_numerator'
    ]
    photo_updates = {k: v for k, v in property_overrides.items() if k in photo_property_list}
    with Session(engine) as session:
        session.query(Photo).filter_by(photo_id=photo_id).update(photo_updates)
        session.commit()

def delete_photo(engine, photo_id):
    """Delete a photo"""
    with Session(engine) as session:
        photo = select_photo(engine, photo_id=photo_id)
        if photo is None:
            raise Exception('Photo not found')
        session.delete(photo)
        session.commit()

def select_edit(engine, edit_id=None, photo_id=None, account_id=None, edit_title=None):
    """Select an edit"""
    with Session(engine) as session:
        if edit_id is not None:
            return session.query(Edit).filter_by(edit_id=edit_id).first()
        if photo_id is not None and \
            account_id is not None and \
            edit_title is not None:
            return session.query(Edit).filter_by(
                photo_id=photo_id,
                account_id=account_id,
                edit_title=edit_title
            ).first()
        return None

def create_edit(
    engine,
    account_id,
    edit_title,
    preview_id=None,
    photo_id=None,
    editor_id=None,
    edit_description=None,
    edit_file_path=None,
    edit_file_extension=None,
    edit_file_size=None,
    edit_width=None,
    edit_height=None
):
    """Create an edit"""
    # pylint: disable=too-many-arguments
    with Session(engine) as session:
        edit = select_edit(
            engine,
            photo_id=photo_id,
            account_id=account_id,
            edit_title=edit_title
        )
        if edit is not None:
            raise Exception(
                f'Edit title in use by account for photo ({edit_title}, {account_id}, {photo_id})'
            )
        edit = Edit(
            account_id=account_id,
            edit_title=edit_title,
            preview_id=preview_id,
            photo_id=photo_id,
            editor_id=editor_id,
            edit_description=edit_description,
            edit_file_path=edit_file_path,
            edit_file_extension=edit_file_extension,
            edit_file_size=edit_file_size,
            edit_width=edit_width,
            edit_height=edit_height
        )
        session.add(edit)
        session.commit()
        session.refresh(edit)
        return edit

def update_edit(
    engine,
    edit_id,
    **property_overrides
):
    """Update an edit"""
    edit_property_list = [
        'account_id',
        'preview_id',
        'photo_id',
        'editor_id',
        'edit_title',
        'edit_description',
        'edit_file_path',
        'edit_file_extension',
        'edit_file_size',
        'edit_width',
        'edit_height'
    ]
    edit_updates = {k: v for k, v in property_overrides if k in edit_property_list}
    with Session(engine) as session:
        session.query(Edit).filter_by(edit_id=edit_id).update(edit_updates)
        session.commit()

def delete_edit(engine, edit_id):
    """Delete an edit"""
    with Session(engine) as session:
        edit = select_edit(engine, edit_id=edit_id)
        if edit is None:
            raise Exception(f'Edit not found ({edit_id})')
        session.delete(edit)
        session.commit()

def select_reply(engine, reply_id):
    """Select a reply"""
    with Session(engine) as session:
        if reply_id is not None:
            return session.query(Reply).filter_by(reply_id=reply_id).first()
        return None

def create_reply(
    engine,
    account_id,
    reply_text,
    photo_id=None,
    edit_id=None
):
    """Create a reply"""
    with Session(engine) as session:
        reply = Reply(
            account_id=account_id,
            reply_text=reply_text,
            photo_id=photo_id,
            edit_id=edit_id
        )
        session.add(reply)
        session.commit()
        session.refresh(reply)
        return reply

def update_reply(engine, reply_id, **property_overrides):
    """Update a reply"""
    with Session(engine) as session:
        reply_property_list = ['reply_text']
        reply_updates = {k: v for k, v in property_overrides if k in reply_property_list}
        session.query(Reply).filter_by(reply_id=reply_id).update(reply_updates)
        session.commit()

def delete_reply(engine, reply_id):
    """Delete a reply"""
    with Session(engine) as session:
        reply = select_reply(engine, reply_id=reply_id)
        if reply is None:
            raise Exception(f'Reply not found ({reply_id})')
        session.delete(reply)
        session.commit()

def select_reaction(engine, reaction_id):
    """Select an reaction"""
    with Session(engine) as session:
        if reaction_id is not None:
            return session.query(Reaction).filter_by(reaction_id=reaction_id).first()
        return None

def create_reaction(
    engine,
    account_id,
    reaction_photo_id=None,
    reaction_edit_id=None,
    reaction_reply_id=None
):
    """Create an reaction"""
    with Session(engine) as session:
        reaction = Reaction(
            account_id=account_id,
            reaction_photo_id=reaction_photo_id,
            reaction_edit_id=reaction_edit_id,
            reaction_reply_id=reaction_reply_id
        )
        session.add(reaction)
        session.commit()
        session.refresh(reaction)
        return reaction

def delete_reaction(engine, reaction_id):
    """Delete an reaction"""
    with Session(engine) as session:
        reaction = select_reaction(engine, reaction_id=reaction_id)
        if reaction is None:
            raise Exception(f'Reaction not found ({reaction_id})')
        session.delete(reaction)
        session.commit()

def create_preview(
    engine,
    preview_file_path,
    preview_file_size,
    preview_width,
    preview_height
):
    """Create a preview"""
    # pylint: disable=too-many-arguments
    with Session(engine) as session:
        preview = Preview(
            preview_file_path=preview_file_path,
            preview_file_size=preview_file_size,
            preview_width=preview_width,
            preview_height=preview_height
        )
        session.add(preview)
        session.commit()
        session.refresh(preview)
        return preview

def update_preview(
    engine,
    preview_id,
    **property_overrides
):
    """Update a preview"""
    preview_property_list = [
        'preview_file_path',
        'preview_file_size',
        'preview_width',
        'preview_height'
    ]
    preview_updates = {k: v for k, v in property_overrides if k in preview_property_list}
    with Session(engine) as session:
        session.query(Preview).filter_by(preview_id=preview_id).update(preview_updates)
        session.commit()

def delete_preview(engine, preview_id):
    """Delete a preview"""
    with Session(engine) as session:
        preview = select_preview(engine, preview_id=preview_id)
        if preview is None:
            raise Exception(f'Preview not found ({preview_id})')
        session.delete(preview)
        session.commit()

def select_tag(engine, tag_id):
    """Select a tag"""
    with Session(engine) as session:
        if tag_id is not None:
            return session.query(Tag).filter_by(tag_id=tag_id).first()
        return None

def create_tag(engine, tag_name):
    """Create a tag"""
    with Session(engine) as session:
        tag = Tag(tag_name=tag_name)
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag

def delete_tag(engine, tag_id):
    """Delete a tag"""
    with Session(engine) as session:
        tag = select_tag(engine, tag_id=tag_id)
        if tag is None:
            raise Exception(f'Tag not found ({tag_id})')
        session.delete(tag)
        session.commit()

def select_editor(engine, editor_id):
    """Select an editor"""
    with Session(engine) as session:
        if editor_id is not None:
            return session.query(Editor).filter_by(editor_id=editor_id).first()
        return None

def create_editor(engine, editor_name, editor_version=None, editor_platform=None):
    """Create an editor"""
    with Session(engine) as session:
        editor = Editor(
            editor_name=editor_name,
            editor_version=editor_version,
            editor_platform=editor_platform
        )
        session.add(editor)
        session.commit()
        session.refresh(editor)
        return editor

def update_editor(engine, editor_id, **property_overrides):
    """Update an editor"""
    with Session(engine) as session:
        editor_property_list = [
            'editor_name',
            'editor_version',
            'editor_platform'
        ]
        editor_updates = {k: v for k, v in property_overrides if k in editor_property_list}
        session.query(Editor).filter_by(editor_id=editor_id).update(editor_updates)
        session.commit()

def delete_editor(engine, editor_id):
    """Delete an editor"""
    with Session(engine) as session:
        editor = select_editor(engine, editor_id=editor_id)
        if editor is None:
            raise Exception(f'Editor not found ({editor_id})')
        session.delete(editor)
        session.commit()

def select_camera(engine, camera_id):
    """Select a camera"""
    with Session(engine) as session:
        if camera_id is not None:
            return session.query(Camera).filter_by(camera_id=camera_id).first()
        return None

def create_camera(engine, manufacturer_id, camera_model):
    """Create a camera"""
    with Session(engine) as session:
        camera = Camera(
            manufacturer_id=manufacturer_id,
            camera_model=camera_model
        )
        session.add(camera)
        session.commit()
        session.refresh(camera)
        return camera

def update_camera(engine, camera_id, **property_overrides):
    """Update a camera"""
    with Session(engine) as session:
        camera_property_list = ['manufacturer_id', 'camera_model']
        camera_updates = {k: v for k, v in property_overrides if k in camera_property_list}
        session.query(Camera).filter_by(camera_id=camera_id).update(camera_updates)
        session.commit()

def delete_camera(engine, camera_id):
    """Delete a camera"""
    with Session(engine) as session:
        camera = select_camera(engine, camera_id=camera_id)
        if camera is None:
            raise Exception(f'Camera not found ({camera_id})')
        session.delete(camera)
        session.commit()

def select_lens(engine, lens_id):
    """Select a lens"""
    with Session(engine) as session:
        if lens_id is not None:
            return session.query(Lens).filter_by(lens_id=lens_id).first()
        return None

def create_lens(
    engine,
    manufacturer_id,
    lens_model,
    aperture_min=None,
    aperture_max=None,
    focal_length_min=None,
    focal_length_max=None
):
    """Create a lens"""
    # pylint: disable=too-many-arguments
    with Session(engine) as session:
        lens = Lens(
            manufacturer_id=manufacturer_id,
            lens_model=lens_model,
            aperture_min=aperture_min,
            aperture_max=aperture_max,
            focal_length_min=focal_length_min,
            focal_length_max=focal_length_max
        )
        session.add(lens)
        session.commit()
        session.refresh(lens)
        return lens

def update_lens(engine, lens_id, **property_overrides):
    """Update a lens"""
    with Session(engine) as session:
        lens_property_list = [
            'manufacturer_id',
            'lens_model',
            'aperture_min',
            'aperture_max',
            'focal_length_min',
            'focal_length_max'
        ]
        lens_updates = {k: v for k, v in property_overrides if k in lens_property_list}
        session.query(Lens).filter_by(lens_id=lens_id).update(lens_updates)
        session.commit()

def delete_lens(engine, lens_id):
    """Delete a lens"""
    with Session(engine) as session:
        lens = select_lens(engine, lens_id=lens_id)
        if lens is None:
            raise Exception(f'Lens not found ({lens_id})')
        session.delete(lens)
        session.commit()

def select_manufacturer(engine, manufacturer_id=None, manufacturer_name=None):
    """Select a manufacturer"""
    with Session(engine) as session:
        if manufacturer_id is not None:
            return session.query(Manufacturer) \
                          .filter_by(manufacturer_id=manufacturer_id) \
                          .first()
        if manufacturer_name is not None:
            return session.query(Manufacturer) \
                          .filter_by(manufacturer_name=manufacturer_name) \
                          .first()
        return None

def create_manufacturer(engine, manufacturer_name):
    """Create a manufacturer"""
    with Session(engine) as session:
        manufacturer = Manufacturer(manufacturer_name=manufacturer_name)
        session.add(manufacturer)
        session.commit()
        session.refresh(manufacturer)
        return manufacturer

def update_manufacturer(engine, manufacturer_id, **property_overrides):
    """Update a manufacturer"""
    with Session(engine) as session:
        manufacturer_property_list = ['manufacturer_name']
        manufacturer_updates = {
            k: v for k, v in property_overrides if k in manufacturer_property_list
        }
        session.query(Manufacturer) \
               .filter_by(manufacturer_id=manufacturer_id) \
               .update(manufacturer_updates)
        session.commit()

def delete_manufacturer(engine, manufacturer_id):
    """Delete a manufacturer"""
    with Session(engine) as session:
        manufacturer = select_manufacturer(engine, manufacturer_id=manufacturer_id)
        if manufacturer is None:
            raise Exception(f'Manufacturer not found ({manufacturer_id})')
        session.delete(manufacturer)
        session.commit()
