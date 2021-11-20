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
| /upvote       | PUT        | create_upvote       | Redis, Postgres     |
| /upvote       | DELETE     | delete_upvote       | Redis, Postgres     |
| /preview      | PUT        | create_preview      | Redis, Postgres     |
| /preview      | POST       | update_preview      | Redis, Postgres     |
| /preview      | DELETE     | delete_preview      | Redis, Postgres     |
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

from flask import Flask, jsonify, request
from flask_graphql import GraphQLView
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from model import Base
from schema import schema
from handlers import (
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
    create_upvote,
    delete_upvote,
    create_preview,
    update_preview,
    delete_preview,
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

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

@app.route('/account', methods=['PUT'])
def handle_create_account():
    """Flask route for creating an account"""
    account_options = request.json
    if account_options is None:
        return 'Bad request', 400
    account_option_keys = account_options.keys()
    if 'account_name' not in account_option_keys or \
       'account_email' not in account_option_keys:
       return 'Bad request', 400

    account = None
    if 'account_role' in account_option_keys:
        account = create_account(
            engine,
            account_options['account_name'],
            account_options['account_email'],
            account_options['account_role']
        )
    else:
        account = create_account(
            engine,
            account_options['account_name'],
            account_options['account_email']
        )

    if account is None:
        return 'Failed to create', 500
    return jsonify({ 'accountId': account.account_id }), 201

@app.route('/account/<account_id>', methods=['POST'])
def handle_update_account(account_id):
    """Flask route for updating an account"""
    account_options = request.json
    if account_options is None:
        return 'Bad request', 400
    update_account(engine, account_id, **account_options)
    return '', 200

@app.route('/account/<account_id>', methods=['DELETE'])
def handle_delete_account(account_id):
    """Flask route for deleting an account"""
    delete_account(engine, account_id)
    return '', 204

@app.route('/photo', methods=['PUT'])
def handle_create_photo():
    """Flask route for creating a photo"""
    photo_options = request.json
    if photo_options is None:
        return 'Bad request', 400
    photo = create_photo(engine, **photo_options)
    if photo is None:
        return 'Failed to create', 500
    return jsonify({ 'photoId': photo.photo_id }), 201

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
        return 'Failed to create', 500
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
        return 'Failed to create', 500
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

@app.route('/upvote', methods=['PUT'])
def handle_create_upvote():
    """Flask route for creating an upvote"""
    upvote_options = request.json
    if upvote_options is None:
        return 'Bad request', 400
    upvote = create_upvote(engine, **upvote_options)
    if upvote is None:
        return 'Failed to create', 500
    return jsonify({ 'upvoteId': upvote.upvote_id }), 201

@app.route('/upvote', methods=['DELETE'])
def handle_delete_upvote():
    """Flask route for deleting an upvote"""
    delete_upvote(engine, upvote_id)
    return '', 204

@app.route('/preview', methods=['PUT'])
def handle_create_preview():
    """Flask route for creating a preview"""
    preview_options = request.json
    if preview_options is None:
        return 'Bad request', 400
    preview = create_preview(engine, **preview_options)
    if preview is None:
        return 'Failed to create', 500
    return jsonify({ 'previewId': preview.preview_id }), 201

@app.route('/preview/<preview_id>', methods=['POST'])
def handle_update_preview(preview_id):
    """Flask route for updating a preview"""
    preview_options = request.json
    if preview_options is None:
        return 'Bad request', 400
    update_preview(engine, preview_id, **preview_options)
    return '', 200

@app.route('/preview/<preview_id>', methods=['DELETE'])
def handle_delete_preview(preview_id):
    """Flask route for deleting a preview"""
    delete_preview(engine, preview_id)
    return '', 204

@app.route('/tag', methods=['PUT'])
def handle_create_tag():
    """Flask route for creating a tag"""
    tag_options = request.json
    if tag_options is None:
        return 'Bad request', 400
    tag = create_tag(engine, **tag_options)
    if tag is None:
        return 'Failed to create', 500
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
        return 'Failed to create', 500
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
        return 'Failed to create', 500
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
        return 'Failed to create', 500
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
        return 'Failed to create', 500
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
