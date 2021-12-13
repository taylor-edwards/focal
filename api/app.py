"""
Flask app with GraphQL interface to underlying
Postgres database connected with SQLAlchemy

Flask endpoints:

+---------------+------------+---------------------+---------------------+
| PATH          | METHOD     | FUNCTION            | SERVICES            |
+---------------+------------+---------------------+---------------------+
| /account      | PUT        | create_account      | Postgres, SendGrid  |
| /account      | POST       | update_account      | Redis, Postgres     |
| /account      | DELETE     | delete_account      | Redis, Postgres     |
| /photo        | PUT        | create_photo        | Redis, Postgres     |
| /photo        | POST       | update_photo        | Redis, Postgres     |
| /photo        | DELETE     | delete_photo        | Redis, Postgres     |
| /edit         | PUT        | create_edit         | Redis, Postgres     |
| /edit         | POST       | update_edit         | Redis, Postgres     |
| /edit         | DELETE     | delete_edit         | Redis, Postgres     |
| /reply        | PUT        | create_reply        | Redis, Postgres     |
| /reply        | POST       | update_reply        | Redis, Postgres     |
| /reply        | DELETE     | delete_reply        | Redis, Postgres     |
| /reaction     | PUT        | create_reaction     | Redis, Postgres     |
| /reaction     | DELETE     | delete_reaction     | Redis, Postgres     |
| /tag          | PUT        | create_tag          | Redis, Postgres     |
| /tag          | DELETE     | delete_tag          | Redis, Postgres     |
| /editor       | PUT        | create_editor       | Redis, Postgres     |
| /editor       | POST       | update_editor       | Redis, Postgres     |
| /editor       | DELETE     | delete_editor       | Redis, Postgres     |
| /camera       | PUT        | create_camera       | Redis, Postgres     |
| /camera       | POST       | update_camera       | Redis, Postgres     |
| /camera       | DELETE     | delete_camera       | Redis, Postgres     |
| /lens         | PUT        | create_lens         | Redis, Postgres     |
| /lens         | POST       | update_lens         | Redis, Postgres     |
| /lens         | DELETE     | delete_lens         | Redis, Postgres     |
| /manufacturer | PUT        | create_manufacturer | Redis, Postgres     |
| /manufacturer | POST       | update_manufacturer | Redis, Postgres     |
| /manufacturer | DELETE     | delete_manufacturer | Redis, Postgres     |
| /session      | POST       | create_session      | Redis, SendGrid     |
| /session      | DELETE     | delete_session      | Redis               |
| /graphql      | POST       | GraphQLView         | Postgres, Redis     |
+---------------+------------+---------------------+---------------------+

Every endpoint performs authentication by comparing for a hash from the API
call's cookie to that of a session in Redis, avoiding the database entirely.

Account creation sends a verification email to supplied email address.
Login sends a magic link to the supplied email address.

Expensive queries' results can be cached in Redis.
"""

import os
import sys
import io
from flask import Flask, jsonify, request
from flask_graphql import GraphQLView
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.utils import secure_filename
from PIL import Image
import json5 as json
import hashlib

from model import Base
from schema import schema
from handlers import (
    select_account,
    create_account,
    update_account,
    delete_account,
    create_photo,
    update_photo,
    delete_photo,
    create_edit,
    update_edit,
    delete_edit,
    create_reply,
    update_reply,
    delete_reply,
    create_reaction,
    delete_reaction,
    create_file,
    delete_file,
    create_tag,
    delete_tag,
    create_editor,
    update_editor,
    delete_editor,
    create_camera,
    update_camera,
    delete_camera,
    create_lens,
    update_lens,
    delete_lens,
    create_manufacturer,
    update_manufacturer,
    delete_manufacturer
)

def hash_file(file):
    BUF_SIZE = 65536 # 64kb chunks
    md5 = hashlib.md5()
    while True:
        data = file.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)
    return md5

def read_extension(file_name):
    return file_name.rsplit('.', 1)[1].lower()

def del_prop(object, property):
    if property in object:
        del object[property]

# Load configuration
with open('../config.json', 'r') as f:
    config = json.load(f)

# Ensure upload directories exist

upload_dir = os.path.join(os.getcwd(), *[secure_filename(p) for p in config['upload_path']])
try:
    os.mkdir(upload_dir)
except FileExistsError:
    pass

# Open a connection to the Postgres database

engine = create_engine('postgresql+psycopg2://focal:asdf@127.0.0.1:5432/focal')
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base.metadata.create_all(engine)
Base.query = db_session.query_property()

# Create Flask app and add API routes

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = upload_dir

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

@app.route('/config/supported_file_extensions', methods=['GET'])
def handle_supported_file_ext():
    if not config:
        return '', 404
    return jsonify(config['supported_file_extensions']), 200

@app.route('/account', methods=['POST'])
def handle_account():
    """Flask route for creating an account"""
    # # Check for existing session
    # session_cookie = request.cookies.get('session')
    # if session_cookie:
    #     if session_cookie exists in Redis and account_email matches
    #         return 'OK', 200
    #     else
    #         # delete cookie
    #         response.set_cookie('session', '', expires=0)
    #         session_cookie
    #         return '', 403

    if request.json is None or 'account_name' not in request.json \
                            or 'account_email' not in request.json:
       return 'Bad request', 400

    name = request.json['account_name']
    if not str.isascii(name) or len(name) < 1:
        return 'Invalid name', 400

    try:
        account_options = {
            'account_name': request.json['account_name'],
            'account_email': request.json['account_email']
        }
        if 'account_role' in request.json:
            account_options['account_role'] = request.json['account_role']
        account = create_account(engine, **account_options)
    except ValueError as err:
        return str(err), 400
    if account is None:
        return 'Error creating account', 500

    # TODO: send email with magic link/code to login

    # request.cookies.set('session', 'mysecurehash')

    return jsonify({ 'accountSafename': account.account_safename }), 201

@app.route('/account/<account_safename>', methods=['POST'])
def handle_update_account(account_safename):
    """Flask route for updating an account"""
    if account_options is None:
        return 'Bad request', 400
    account = select_account(engine, account_safename=account_safename)
    if account is None:
        return 'Account not found', 404
    account_options = {}
    if 'account_name' in request.json:
        account_options['account_name'] = request.json['account_role']
    if 'account_email' in request.json:
        account_options['account_email'] = request.json['account_email']
    if account_options != {}:
        update_account(engine, account.account_id, **account_options)
    return '', 200

@app.route('/account/<account_safename>', methods=['DELETE'])
def handle_delete_account(account_safename):
    """Flask route for deleting an account"""
    account = select_account(engine, account_safename=account_safename)
    if account is None:
        return 'Account not found', 404
    delete_account(engine, account.account_id)
    return '', 204

@app.route('/photo', methods=['PUT'])
def handle_create_photo():
    """Flask route for creating a photo"""
    photo_options = {}
    created_camera_id = None
    created_camera_manufacturer_id = None
    created_lens_id = None
    created_lens_manufacturer_id = None

    if request.form is None:
        return 'Bad request', 400
    for key in request.form:
        v = request.form[key]
        if v != 'null':
            photo_options[key] = v

    account = select_account(engine, account_safename=photo_options['account_safename'])
    if account is None:
        return 'Account not found', 404
    # Replace account_safename with account_id
    photo_options['account_id'] = account.account_id
    del_prop(photo_options, 'account_safename')

    if ('photo_title' not in photo_options or len(photo_options['photo_title']) == 0) \
       and ('photo_text' not in photo_options or len(photo_options['photo_text']) == 0):
        return 'Neither title nor description found', 400

    if 'raw_file' not in request.files and 'preview_file' not in request.files:
        return 'Attachment not found', 400

    # Insert camera
    # """Create camera and manufacturer rows"""
    try:
        # Get camera ID from request or after insertion
        if 'camera_id' not in photo_options and 'camera_model' in photo_options \
                                            and len(photo_options['camera_model']) > 0:
            camera_options = {
                'camera_model': photo_options['camera_model']
            }
            # Get manufacturer ID from request or after insertion
            if camera_manufacturer_id in photo_options:
                camera_options['manufacturer_id'] = photo_options['camera_manufacturer_id']
            elif camera_manufacturer_name in photo_options \
                 and len(photo_options['camera_manufacturer_name']) > 0:
                # Insert manufacturer row
                mfr = create_manufacturer(
                    engine,
                    manufacturer_name=photo_options['camera_manufacturer_name']
                )
                if mfr is None:
                    raise ValueError('Error creating manufacturer', 409)
                camera_options['manufacturer_id'] = mfr.manufacturer_id
                created_camera_manufacturer_id = mfr.manufacturer_id
            if 'manufacturer_id' in camera_options:
                # Insert camera row
                camera = create_camera(engine, **camera_options)
                if camera is None:
                    raise ValueError('Error creating camera', 409)
                photo_options['camera_id'] = camera.camera_id
                created_camera_id = camera.camera_id
    except Exception as err:
        print('Could not process camera equipment', err)
        # clean up any created rows
        if created_camera_id is not None:
            delete_camera(engine, created_camera_id)
            created_camera_id = None
        if created_camera_manufacturer_id is not None:
            delete_manufacturer(engine, created_camera_manufacturer_id)
            created_camera_manufacturer_id = None
        pass # tolerate camera failure while posting
    del_prop(photo_options, 'camera_model')
    del_prop(photo_options, 'camera_manufacturer_id')
    del_prop(photo_options, 'camera_manufacturer_name')

    # Insert lens
    # """Create lens and manufacturer rows"""
    try:
        # Get camera ID from request or after insertion
        if 'lens_id' not in photo_options and 'lens_model' in photo_options \
                                          and len(photo_options['lens_model']) > 0:
            lens_options = {
                'lens_model': photo_options['lens_model']
            }
            if 'aperture_min' in photo_options:
                lens_options['aperture_min'] = photo_options['lens_aperture_min']
            if 'aperture_max' in photo_options:
                lens_options['aperture_max'] = photo_options['lens_aperture_max']
            if 'focal_length_min' in photo_options:
                lens_options['focal_length_min'] = photo_options['lens_focal_length_min']
            if 'focal_length_max' in photo_options:
                lens_options['focal_length_max'] = photo_options['lens_focal_length_max']
            # Get manufacturer ID from request or after insertion
            if lens_manufacturer_id in photo_options:
                lens_options['manufacturer_id'] = photo_options['lens_manufacturer_id']
            elif 'lens_manufacturer_name' in photo_options \
                  and len(photo_options['lens_manufacturer_name']) > 0:
                # Insert manufacturer row
                mfr = create_manufacturer(
                    engine,
                    manufacturer_name=photo_options['lens_manufacturer_name']
                )
                if mfr is None:
                    raise ValueError('Error creating manufacturer', 409)
                lens_options['manufacturer_id'] = mfr.manufacturer_id
                created_lens_manufacturer_id = mfr.manufacturer_id
            if 'manufacturer_id' in lens_options:
                # Insert lens row
                lens = create_lens(engine, **lens_options)
                if lens is None:
                    raise ValueError('Error creating lens', 409)
                photo_options['lens_id'] = lens.lens_id
                created_lens_id = lens.lens_id
    except Exception as err:
        print('Could not process lens equipment', err)
        # clean up any created rows
        if created_lens_id is not None:
            delete_lens(created_lens_id)
            created_lens_id = None
        if created_lens_manufacturer_id is not None and \
           created_lens_manufacturer_id != created_camera_manufacturer_id:
            # don't delete the camera's manufacturer in case the camera row
            # insertion was successful but the lens insertion failed
            delete_manufacturer(created_lens_manufacturer_id)
            created_lens_manufacturer_id = None
        pass # tolerate lens failure while posting
    del_prop(photo_options, 'lens_model')
    del_prop(photo_options, 'lens_aperture_min')
    del_prop(photo_options, 'lens_aperture_max')
    del_prop(photo_options, 'lens_focal_length_min')
    del_prop(photo_options, 'lens_focal_length_max')
    del_prop(photo_options, 'lens_manufacturer_id')
    del_prop(photo_options, 'lens_manufacturer_name')

    # Attach files
    # """Process raw and preview files"""
    raw_file_path = None
    preview_file_path = None
    try:
        if 'preview_file' in request.files:
            file = request.files['preview_file']
            if '.' not in file.filename:
                raise ValueError('Extension not found', 415)

            extension = read_extension(file.filename)
            if extension not in config['supported_file_extensions']['preview_file']:
                raise ValueError(f'Unsupported extension ({extension})', 415)

            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                secure_filename(hash_file(file).hexdigest() + '.' + config['preview_image_format'])
            )
            if os.path.exists(file_path):
                raise FileExistsError(f'Preview file is a likely duplicate of {str(file_path)}')
            image = Image.open(file)
            image.thumbnail(config['preview_image_size'])
            image.save(file_path)
            preview_file_path = file_path
            size = os.stat(file_path).st_size

            preview_entry = create_file(engine,
                file_path=str(file_path), file_name=str(file.filename),
                file_extension=config['preview_image_format'], file_size=size,
                image_width=image.size[0], image_height=image.size[1])
            if preview_entry is None:
                raise Exception('Error creating preview')
            photo_options['preview_file_id'] = preview_entry.file_id
    except Exception as err:
        print('Could not process photo preview file. Error:', str(err))
        if preview_file_path is not None:
            os.remove(preview_file_path)
            preview_file_path = None
        if 'preview_file_id' in photo_options:
            delete_file(engine, photo_options['preview_file_id'])
            del_prop(photo_options, 'preview_file_id')

    try:
        if 'raw_file' in request.files:
            file = request.files['raw_file']
            if '.' not in file.filename:
                raise ValueError('Extension not found', 415)

            extension = read_extension(file.filename)
            if extension not in config['supported_file_extensions']['raw_file']:
                raise ValueError(f'Unsupported extension ({extension})', 415)

            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                secure_filename(hash_file(file).hexdigest() + '.' + extension)
            )
            if os.path.exists(file_path):
                raise FileExistsError(f'Preview file is a likely duplicate of {str(file_path)}')
            file.save(file_path)
            raw_file_path = file_path
            size = os.stat(file_path).st_size

            raw_entry = create_file(engine, file_path=str(file_path), file_name=str(file.filename),
                                    file_extension=extension, file_size=size)
            if raw_entry is None:
                raise Exception('Error creating raw file')
            photo_options['raw_file_id'] = raw_entry.file_id
            # if 'preview_file_id' not in photo_options:
            #     # try to extract an embedded image from the raw file to use as the preview
            #     try:
            #         # get thumbnail image
            #         # write to disk
            #         # insert into File table in database
            #         # set photo_options['preview_file_id'] to the new File.file_id
            #         # set preview_file_path = file_path
            #     except Exception as err:
            #         print('Failed to extract thumbnail from raw file')
    except Exception as err:
        print('Could not process photo raw file. Error:', str(err))
        if raw_file_path is not None:
            os.remove(raw_file_path)
            raw_file_path = None
        if 'raw_file_id' in photo_options:
            delete_file(engine, photo_options['raw_file_id'])
            del_prop(photo_options, 'raw_file_id')

    try:
        if not ('preview_file_id' in photo_options or 'raw_file_id' in photo_options):
            raise ValueError('Photo posts must include at least one raw file or preview image')
        # Insert photo row and return its photo_id
        photo = create_photo(engine, **photo_options)
        if photo is None:
            raise Exception('Error creating photo')
        return jsonify({ 'photoId': photo.photo_id }), 201
    except Exception as err:
        print('Could not create_photo:', str(err))

        # delete any files written to disk
        if preview_file_path is not None:
            os.remove(preview_file_path)
            preview_file_path = None
        if raw_file_path is not None:
            os.remove(raw_file_path)
            raw_file_path = None

        # back out any database insertions
        if 'preview_file_id' in photo_options:
            delete_file(engine, photo_options['preview_file_id'])
            del_prop(photo_options, 'preview_file_id')
        if 'raw_file_id' in photo_options:
            delete_file(engine, photo_options['raw_file_id'])
            del_prop(photo_options, 'raw_file_id')
        if created_camera_id is not None:
            delete_camera(engine, created_camera_id)
        if created_camera_manufacturer_id is not None:
            delete_manufacturer(engine, created_camera_manufacturer_id)
        if created_lens_id is not None:
            delete_lens(created_lens_id)
        if created_lens_manufacturer_id is not None:
            delete_manufacturer(created_lens_manufacturer_id)

        return str(err), 500

    # Create notifications
    # actor_id = account.account_id
    # follower_ids = select follower_id from account_follow where following_id == actor_id
    # notify_options = {}
    # for each id in follower_ids:
    #     insert notification

@app.route('/photo/<photo_id>', methods=['POST'])
def handle_update_photo(photo_id):
    """Flask route for updating a photo"""
    photo_options = request.json
    if photo_options is None:
        return 'Bad request', 400
    update_photo(engine, photo_id, **photo_options)
    return '', 200

@app.route('/photo/<photo_id>', methods=['DELETE'])
def handle_delete_photo(photo_id):
    """Flask route for deleting a photo"""
    delete_photo(engine, photo_id)
    return '', 204

@app.route('/edit', methods=['PUT'])
def handle_create_edit():
    """Flask route for creating an edit"""
    edit_options = request.json
    if edit_options is None:
        return 'Bad request', 400
    edit = create_edit(engine, **edit_options)
    if edit is None:
        return 'Error creating edit', 500
    return jsonify({ 'editId': edit.edit_id }), 201

@app.route('/edit/<edit_id>', methods=['POST'])
def handle_update_edit(edit_id):
    """Flask route for updating an edit"""
    edit_options = request.json
    if edit_options is None:
        return 'Bad request', 400
    update_edit(engine, edit_id, **edit_options)
    return '', 200

@app.route('/edit/<edit_id>', methods=['DELETE'])
def handle_delete_edit(edit_id):
    """Flask route for deleting an edit"""
    delete_edit(engine, edit_id)
    return '', 204

@app.route('/reply', methods=['PUT'])
def handle_create_reply():
    """Flask route for creating a reply"""
    reply_options = request.json
    if reply_options is None:
        return 'Bad request', 400
    reply = create_reply(engine, **reply_options)
    if reply is None:
        return 'Error creating reply', 500
    return jsonify({ 'replyId': reply.reply_id }), 201

@app.route('/reply/<reply_id>', methods=['POST'])
def handle_update_reply(reply_id):
    """Flask route for updating a reply"""
    reply_options = request.json
    if reply_options is None:
        return 'Bad request', 400
    update_reply(engine, reply_id, **reply_options)
    return '', 200

@app.route('/reply/<reply_id>', methods=['DELETE'])
def handle_delete_reply(reply_id):
    """Flask route for deleting a reply"""
    delete_reply(engine, reply_id)
    return '', 204

@app.route('/reaction', methods=['PUT'])
def handle_create_reaction():
    """Flask route for creating an reaction"""
    reaction_options = request.json
    if reaction_options is None:
        return 'Bad request', 400
    reaction = create_reaction(engine, **reaction_options)
    if reaction is None:
        return 'Error creating reaction', 500
    return jsonify({ 'reactionId': reaction.reaction_id }), 201

@app.route('/reaction', methods=['DELETE'])
def handle_delete_reaction():
    """Flask route for deleting an reaction"""
    delete_reaction(engine, reaction_id)
    return '', 204

@app.route('/tag', methods=['PUT'])
def handle_create_tag():
    """Flask route for creating a tag"""
    tag_options = request.json
    if tag_options is None:
        return 'Bad request', 400
    tag = create_tag(engine, **tag_options)
    if tag is None:
        return 'Error creating tag', 500
    return jsonify({ 'tagId': tag.tag_id }), 201

@app.route('/tag/<tag_id>', methods=['DELETE'])
def handle_delete_tag(tag_id):
    """Flask route for deleting a tag"""
    delete_tag(engine, tag_id)
    return '', 204

@app.route('/editor', methods=['PUT'])
def handle_create_editor():
    """Flask route for creating an editor"""
    editor_options = request.json
    if editor_options is None:
        return 'Bad request', 400
    editor = create_editor(engine, **editor_options)
    if editor is None:
        return 'Error creating editor', 500
    return jsonify({ 'editorId': editor.editor_id }), 201

@app.route('/editor/<editor_id>', methods=['POST'])
def handle_update_editor(editor_id):
    """Flask route for updating an editor"""
    editor_options = request.json
    if editor_options is None:
        return 'Bad request', 400
    update_editor(engine, editor_id, **editor_options)
    return '', 200

@app.route('/editor/<editor_id>', methods=['DELETE'])
def handle_delete_editor(editor_id):
    """Flask route for deleting an editor"""
    delete_editor(engine, editor_id)
    return '', 204

@app.route('/camera', methods=['PUT'])
def handle_create_camera():
    """Flask route for creating a camera"""
    camera_options = request.json
    if camera_options is None:
        return 'Bad request', 400
    camera = create_camera(engine, **camera_options)
    if camera is None:
        return 'Error creating camera', 500
    return jsonify({ 'cameraId': camera.camera_id }), 201

@app.route('/camera/<camera_id>', methods=['POST'])
def handle_update_camera(camera_id):
    """Flask route for updating a camera"""
    camera_options = request.json
    if camera_options is None:
        return 'Bad request', 400
    update_camera(engine, camera_id, **camera_options)
    return '', 200

@app.route('/camera/<camera_id>', methods=['DELETE'])
def handle_delete_camera(camera_id):
    """Flask route for deleting a camera"""
    delete_camera(engine, camera_id)
    return '', 204

@app.route('/lens', methods=['PUT'])
def handle_create_lens():
    """Flask route for creating a lens"""
    lens_options = request.json
    if lens_options is None:
        return 'Bad request', 400
    lens = create_lens(engine, **lens_options)
    if lens is None:
        return 'Error creating lens', 500
    return jsonify({ 'lensId': lens.lens_id }), 201

@app.route('/lens/<lens_id>', methods=['POST'])
def handle_update_lens(lens_id):
    """Flask route for updating a lens"""
    lens_options = request.json
    if lens_options is None:
        return 'Bad request', 400
    update_lens(engine, lens_id, **lens_options)
    return '', 200

@app.route('/lens/<lens_id>', methods=['DELETE'])
def handle_delete_lens(lens_id):
    """Flask route for deleting a lens"""
    delete_lens(engine, lens_id)
    return '', 204

@app.route('/manufacturer', methods=['PUT'])
def handle_create_manufacturer():
    """Flask route for creating a manufacturer"""
    manufacturer_options = request.json
    if manufacturer_options is None:
        return 'Bad request', 400
    manufacturer = create_manufacturer(engine, **manufacturer_options)
    if manufacturer is None:
        return 'Error creating manufacturer', 500
    return jsonify({ 'manufacturerId': manufacturer.manufacturer_id }), 201

@app.route('/manufacturer/<manufacturer_id>', methods=['POST'])
def handle_update_manufacturer(manufacturer_id):
    """Flask route for updating a manufacturer"""
    manufacturer_options = request.json
    if manufacturer_options is None:
        return 'Bad request', 400
    update_manufacturer(engine, manufacturer_id, **manufacturer_options)
    return '', 200

@app.route('/manufacturer/<manufacturer_id>', methods=['DELETE'])
def handle_delete_manufacturer(manufacturer_id):
    """Flask route for deleting a manufacturer"""
    delete_manufacturer(engine, manufacturer_id)
    return '', 204

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Disconnect database session on shutdown"""
    if exception:
        print(exception)
    db_session.remove()

if __name__ == '__main__':
    app.run()
