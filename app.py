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
import db

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
def create_account():
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
        account = db.create_account(
            engine,
            account_options['account_name'],
            account_options['account_email'],
            account_options['account_role']
        )
    else:
        account = db.create_account(
            engine,
            account_options['account_name'],
            account_options['account_email']
        )

    if account is None:
        return 'Failed to create', 500
    return jsonify({ 'accountId': account.account_id }), 201

@app.route('/account/<account_id>', methods=['POST'])
def update_account(account_id):
    """Flask route for updating an account"""
    account_options = request.json
    if account_options is None:
        return 'Bad request', 400
    db.update_account(engine, account_id, **account_options)
    return '', 200

@app.route('/account/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    """Flask route for deleting an account"""
    db.delete_account(engine, account_id)
    return '', 204

@app.route('/photo', methods=['PUT'])
def create_photo():
    """Flask route for creating a photo"""
    photo_options = request.json
    if photo_options is None:
        return 'Bad request', 400
    photo = db.create_photo(engine, **photo_options)
    if photo is None:
        return 'Failed to create', 500
    return jsonify({ 'photoId': photo.photo_id }), 201

@app.route('/photo/<photo_id>', methods=['POST'])
def update_photo(photo_id):
    """Flask route for updating a photo"""
    photo_options = request.json
    if photo_options is None:
        return 'Bad request', 400
    db.update_photo(engine, photo_id, **photo_options)
    return '', 200

@app.route('/photo/<photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    """Flask route for deleting a photo"""
    db.delete_photo(engine, photo_id)
    return '', 204

@app.route('/edit', methods=['PUT'])
def create_edit():
    """Flask route for creating an edit"""
    edit_options = request.json
    if edit_options is None:
        return 'Bad request', 400
    edit = db.create_edit(engine, **edit_options)
    if edit is None:
        return 'Failed to create', 500
    return jsonify({ 'editId': edit.edit_id }), 201

@app.route('/edit/<edit_id>', methods=['POST'])
def update_edit(edit_id):
    """Flask route for updating an edit"""
    edit_options = request.json
    if edit_options is None:
        return 'Bad request', 400
    db.update_edit(engine, edit_id, **edit_options)
    return '', 200

@app.route('/edit/<edit_id>', methods=['DELETE'])
def delete_edit(edit_id):
    """Flask route for deleting an edit"""
    db.delete_edit(engine, edit_id)
    return '', 204

@app.route('/reply', methods=['PUT'])
def create_reply():
    """Flask route for creating a reply"""
    reply_options = request.json
    if reply_options is None:
        return 'Bad request', 400
    reply = db.create_reply(engine, **reply_options)
    if reply is None:
        return 'Failed to create', 500
    return jsonify({ 'replyId': reply.reply_id }), 201

@app.route('/reply/<reply_id>', methods=['POST'])
def update_reply(reply_id):
    """Flask route for updating a reply"""
    reply_options = request.json
    if reply_options is None:
        return 'Bad request', 400
    db.update_reply(engine, reply_id, **reply_options)
    return '', 200

@app.route('/reply/<reply_id>', methods=['DELETE'])
def delete_reply(reply_id):
    """Flask route for deleting a reply"""
    db.delete_reply(engine, reply_id)
    return '', 204

@app.route('/upvote', methods=['PUT'])
def create_upvote():
    """Flask route for creating an upvote"""
    upvote_options = request.json
    if upvote_options is None:
        return 'Bad request', 400
    upvote = db.create_upvote(engine, **upvote_options)
    if upvote is None:
        return 'Failed to create', 500
    return jsonify({ 'upvoteId': upvote.upvote_id }), 201

@app.route('/upvote', methods=['DELETE'])
def delete_upvote():
    """Flask route for deleting an upvote"""
    db.delete_upvote(engine, upvote_id)
    return '', 204

@app.route('/preview', methods=['PUT'])
def create_preview():
    """Flask route for creating a preview"""
    preview_options = request.json
    if preview_options is None:
        return 'Bad request', 400
    preview = db.create_preview(engine, **preview_options)
    if preview is None:
        return 'Failed to create', 500
    return jsonify({ 'previewId': preview.preview_id }), 201

@app.route('/preview/<preview_id>', methods=['POST'])
def update_preview(preview_id):
    """Flask route for updating a preview"""
    preview_options = request.json
    if preview_options is None:
        return 'Bad request', 400
    db.update_preview(engine, preview_id, **preview_options)
    return '', 200

@app.route('/preview/<preview_id>', methods=['DELETE'])
def delete_preview(preview_id):
    """Flask route for deleting a preview"""
    db.delete_preview(engine, preview_id)
    return '', 204

@app.route('/tag', methods=['PUT'])
def create_tag():
    """Flask route for creating a tag"""
    tag_options = request.json
    if tag_options is None:
        return 'Bad request', 400
    tag = db.create_tag(engine, **tag_options)
    if tag is None:
        return 'Failed to create', 500
    return jsonify({ 'tagId': tag.tag_id }), 201

@app.route('/tag/<tag_id>', methods=['POST'])
def update_tag(tag_id):
    """Flask route for updating a tag"""
    tag_options = request.json
    if tag_options is None:
        return 'Bad request', 400
    db.update_tag(engine, tag_id, **tag_options)
    return '', 200

@app.route('/tag/<tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    """Flask route for deleting a tag"""
    db.delete_tag(engine, tag_id)
    return '', 204

@app.route('/editor', methods=['PUT'])
def create_editor():
    """Flask route for creating an editor"""
    editor_options = request.json
    if editor_options is None:
        return 'Bad request', 400
    editor = db.create_editor(engine, **editor_options)
    if editor is None:
        return 'Failed to create', 500
    return jsonify({ 'editorId': editor.editor_id }), 201

@app.route('/editor/<editor_id>', methods=['POST'])
def update_editor(editor_id):
    """Flask route for updating an editor"""
    editor_options = request.json
    if editor_options is None:
        return 'Bad request', 400
    db.update_editor(engine, editor_id, **editor_options)
    return '', 200

@app.route('/editor/<editor_id>', methods=['DELETE'])
def delete_editor(editor_id):
    """Flask route for deleting an editor"""
    db.delete_editor(engine, editor_id)
    return '', 204

@app.route('/camera', methods=['PUT'])
def create_camera():
    """Flask route for creating a camera"""
    camera_options = request.json
    if camera_options is None:
        return 'Bad request', 400
    camera = db.create_camera(engine, **camera_options)
    if camera is None:
        return 'Failed to create', 500
    return jsonify({ 'cameraId': camera.camera_id }), 201

@app.route('/camera/<camera_id>', methods=['POST'])
def update_camera(camera_id):
    """Flask route for updating a camera"""
    camera_options = request.json
    if camera_options is None:
        return 'Bad request', 400
    db.update_camera(engine, camera_id, **camera_options)
    return '', 200

@app.route('/camera/<camera_id>', methods=['DELETE'])
def delete_camera(camera_id):
    """Flask route for deleting a camera"""
    db.delete_camera(engine, camera_id)
    return '', 204

@app.route('/lens', methods=['PUT'])
def create_lens():
    """Flask route for creating a lens"""
    lens_options = request.json
    if lens_options is None:
        return 'Bad request', 400
    lens = db.create_lens(engine, **lens_options)
    if lens is None:
        return 'Failed to create', 500
    return jsonify({ 'lensId': lens.lens_id }), 201

@app.route('/lens/<lens_id>', methods=['POST'])
def update_lens(lens_id):
    """Flask route for updating a lens"""
    lens_options = request.json
    if lens_options is None:
        return 'Bad request', 400
    db.update_lens(engine, lens_id, **lens_options)
    return '', 200

@app.route('/lens/<lens_id>', methods=['DELETE'])
def delete_lens(lens_id):
    """Flask route for deleting a lens"""
    db.delete_lens(engine, lens_id)
    return '', 204

@app.route('/manufacturer', methods=['PUT'])
def create_manufacturer():
    """Flask route for creating a manufacturer"""
    manufacturer_options = request.json
    if manufacturer_options is None:
        return 'Bad request', 400
    manufacturer = db.create_manufacturer(engine, **manufacturer_options)
    if manufacturer is None:
        return 'Failed to create', 500
    return jsonify({ 'manufacturerId': manufacturer.manufacturer_id }), 201

@app.route('/manufacturer/<manufacturer_id>', methods=['POST'])
def update_manufacturer(manufacturer_id):
    """Flask route for updating a manufacturer"""
    manufacturer_options = request.json
    if manufacturer_options is None:
        return 'Bad request', 400
    db.update_manufacturer(engine, manufacturer_id, **manufacturer_options)
    return '', 200

@app.route('/manufacturer/<manufacturer_id>', methods=['DELETE'])
def delete_manufacturer(manufacturer_id):
    """Flask route for deleting a manufacturer"""
    db.delete_manufacturer(engine, manufacturer_id)
    return '', 204

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Disconnect database session on shutdown"""
    if exception:
        print(exception)
    db_session.remove()

if __name__ == '__main__':
    app.run()
