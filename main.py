"""
Focal test bootstrap

Create, update and delete data to test database integration.
"""

import sys
# from time import sleep
# from db import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from model import Base
from db import (
    select_account,
    create_account,
    update_account,
    delete_account,
    select_photo,
    create_photo,
    update_photo,
    delete_photo,
    # select_edit,
    create_edit,
    # update_edit,
    # delete_edit,
    # select_reply,
    # create_reply,
    # update_reply,
    # delete_reply,
    # select_upvote,
    # create_upvote,
    # delete_upvote,
    # select_tag,
    # create_tag,
    # delete_tag,
    # select_editor,
    create_editor,
    # update_editor,
    # delete_editor,
    # select_camera,
    create_camera,
    # update_camera,
    # delete_camera,
    # select_lens,
    create_lens,
    # update_lens,
    # delete_lens,
    select_manufacturer,
    create_manufacturer,
    # update_manufacturer,
    # delete_manufacturer
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





# Create and modify some accounts

try:
    create_account(
        engine, account_name='chumpy', account_email='chumpy@focal.pics', account_role='admin'
    )
    accounts = [
        create_account(engine, account_name=name, account_email=email) for (name, email) in [
            ('skeletor', 'skeletor@focal.pics'),
            ('nacho', 'nacho@focal.pics'),
            ('jojo', 'jojo@focal.pics'),
            ('dio', 'dio@focal.pics'),
            ('dk', 'dk@focal.pics'),
            ('mario', 'mario@focal.pics'),
            ('bojack', 'bojack@focal.pics'),
            ('daisy', 'daisy@focal.pics'),
            ('-xX.DemonHunter.Xx-', '-xX.DemonHunter.Xx-@focal.pics'),
            ('p3n15', 'p3n15@focal.pics'),
            ('8ball', '8ball@focal.pics'),
            ('fuigi', 'fuigi@focal.pics'),
            ('Don Lane', 'don.lane@focal.pics'),
            ('wayne', 'wayne@focal.pics'),
            ('spiderman', 'spiderman@focal.pics'),
        ]
    ]
except Exception as err: # pylint: disable=broad-except
    print('Create account exception:', err)

skeletor = select_account(engine, account_email='skeletor@focal.pics')
nacho = select_account(engine, account_name='nacho')
eightball = select_account(engine, account_name='8ball')
penuser = select_account(engine, account_name='p3n15')

try:
    if skeletor:
        update_account(
            engine, account_id=skeletor.account_id, account_role='admin', is_verified=True
        )
    if nacho:
        update_account(engine, account_id=nacho.account_id, account_email='cheese@focal.pics')
    if eightball:
        update_account(engine, account_id=eightball.account_id, is_verified=True)
except Exception as err: # pylint: disable=broad-except
    print('Update account exception:', err)

try:
    if penuser:
        delete_account(engine, account_id=penuser.account_id)
except Exception as err: # pylint: disable=broad-except
    print('Delete account exception:', err)





# Create and modify some photos

try:
    if skeletor:
        skeletor_photos = [create_photo(
            engine,
            account_id=skeletor.account_id,
            photo_title=title,
            raw_file_path=file_path,
            raw_file_size=file_size,
            raw_file_extension=file_ext
        ) for (title, file_path, file_ext, file_size) in [
            ('Castle Grayskull', '/path/to/skeletor_castle_grayskull.cr2', 'CR2', 5000),
            ('Deathwish for He-Man', '/path/to/skeletor_death_to_he_man.cr2', 'CR2', 8340),
            ('Daily carry', '/path/to/daily_carry.cr2', 'CR2', 2834)
        ]]
    if nacho:
        nacho_photos = [create_photo(
            engine,
            account_id=nacho.account_id,
            photo_title=title,
            raw_file_path=file_path,
            raw_file_size=file_size,
            raw_file_extension=file_ext
        ) for (title, file_path, file_ext, file_size) in [
            ('Nachos!!', '/path/to/nacho_nachos.raf', 'RAF', 12000),
            ('How much cheese is too much?', '/path/to/nacho_how_much_cheese_is_too_much.raf',
                'RAF', 8340),
            ('SPICY CHIP', '/path/to/spicy_chip.raf', 'RAF', 9163),
            ('hawt sawce', '/path/to/hawt_sawce.raf', 'RAF', 3857)
        ]]
    if eightball:
        eightball_photos = [create_photo(
            engine,
            account_id=eightball.account_id,
            photo_title=title,
            raw_file_path=file_path,
            raw_file_size=file_size,
            raw_file_extension=file_ext
        ) for (title, file_path, file_ext, file_size) in [
            ('Poole greene', '/path/to/eightball_poole_greene.tiff', 'TIFF', 2000),
            ('The Set Up', '/path/to/eightball_the_set_up.tiff', 'TIFF', 8340),
            ('8', '/path/to/8.tiff', 'TIFF', 2034)
        ]]
except Exception as err: # pylint: disable=broad-except
    print('Create photo exception:', err)


try:
    if nacho:
        photo = select_photo(
            engine,
            account_id=nacho.account_id,
            photo_title='How much cheese is too much?'
        )
        if photo:
            update_photo(engine, photo_id=photo.photo_id, photo_description='TOO MUCH!!!')
except Exception as err: # pylint: disable=broad-except
    print('Update photo exception:', err)

try:
    if skeletor:
        photo = select_photo(
            engine,
            account_id=skeletor.account_id,
            photo_title='Deathwish for He-Man'
        )
        if photo:
            delete_photo(engine, photo.photo_id)
except Exception as err: # pylint: disable=broad-except
    print('Delete photo exception:', err)






# Create and modify some edits

try:
    if nacho:
        photo = select_photo(
            engine,
            account_id=nacho.account_id,
            photo_title='How much cheese is too much?'
        )
        if photo:
            nacho_cheese_edits = [create_edit(
                engine,
                account_id=nacho.account_id,
                photo_id=photo.photo_id,
                edit_title=edit_title,
                edit_file_path=file_path,
                edit_file_extension=file_ext,
                edit_file_size=file_size
            ) for (edit_title, file_path, file_ext, file_size) in [
                ('Insta\'d washout filter', '/path/to/nacho_insta_d_washout_filter.xml',
                    'XML', 519),
                ('Nunsplash', '/path/to/nacho_nunsplash.xml', 'XML', 821)
            ]]
            if skeletor:
                skeletor_cheese_edit = create_edit(
                    engine,
                    account_id=skeletor.account_id,
                    photo_id=photo.photo_id,
                    edit_title='Artsy shot of nachos',
                    edit_file_path='/path/to/skeletor_artsy_shot_of_nachos.mie',
                    edit_file_extension='MIE',
                    edit_file_size=337
                )
    if skeletor:
        photo = select_photo(
            engine,
            account_id=skeletor.account_id,
            photo_title='Castle Grayskull'
        )
        if photo:
            skeletor_castle_edits = [create_edit(
                engine,
                account_id=skeletor.account_id,
                photo_id=photo.photo_id,
                edit_title=edit_title,
                edit_file_path=file_path,
                edit_file_extension=file_ext,
                edit_file_size=file_size
            ) for (edit_title, file_path, file_ext, file_size) in [
                ('Daylight', '/path/to/skeletor_daylight.xml', 'XML', 482),
                ('Simulated night', '/path/to/skeletor_simulated_night.xml', 'XML', 655)
            ]]
except Exception as err: # pylint: disable=broad-except
    print('Create edit exception:', err)

try:
    pass
except Exception as err: # pylint: disable=broad-except
    print('Update edit exception:', err)

try:
    pass
except Exception as err: # pylint: disable=broad-except
    print('Delete edit exception:', err)






# Create and modify some replies

try:
    pass
except Exception as err: # pylint: disable=broad-except
    print('Create reply exception:', err)

try:
    pass
except Exception as err: # pylint: disable=broad-except
    print('Update reply exception:', err)

try:
    pass
except Exception as err: # pylint: disable=broad-except
    print('Delete reply exception:', err)






# Create and modify some upvotes

try:
    pass
except Exception as err: # pylint: disable=broad-except
    print('Create upvote exception:', err)

try:
    pass
except Exception as err: # pylint: disable=broad-except
    print('Update upvote exception:', err)

try:
    pass
except Exception as err: # pylint: disable=broad-except
    print('Delete upvote exception:', err)




# Create some editors
try:
    editors = [create_editor(engine, editor_name) for editor_name in [
        'Lightroom',
        'Darktable',
        'Aperture',
        'Apple Photos',
        'Photoshop',
        'Gimp',
        'RawTherapee',
        'Pinta'
    ]]
except Exception as err: # pylint: disable=broad-except
    print('Create editor exception:', err)


# Create some manufacturers
try:
    manufacturers = [create_manufacturer(engine, name) for name in [
        'Canon',
        'Nikon',
        'Fujifilm',
        'Sony',
        'Rokinon',
        'Fujinon',
        'Leica',
        'Panasonic',
        'Instax'
    ]]
except Exception as err: # pylint: disable=broad-except
    print('Create manufacturer exception:', err)


canon_manufacturer = select_manufacturer(engine, manufacturer_name='Canon')
nikon_manufacturer = select_manufacturer(engine, manufacturer_name='Nikon')
fujifilm_manufacturer = select_manufacturer(engine, manufacturer_name='Fujifilm')
rokinon_manufacturer = select_manufacturer(engine, manufacturer_name='Rokinon')

# Create some cameras
try:
    cameras = [create_camera(
        engine,
        manufacturer_id=manufacturer_id,
        camera_model=camera_model
    ) for (manufacturer_id, camera_model) in [
        (canon_manufacturer.manufacturer_id, 'Rebel T5i'),
        (nikon_manufacturer.manufacturer_id, 'D850'),
        (fujifilm_manufacturer.manufacturer_id, 'XT-3')
    ]]
except Exception as err: # pylint: disable=broad-except
    print('Create camera exception:', err)


# Create some lenses
try:
    lenses = [
        create_lens(engine, manufacturer_id, lens_model) for (manufacturer_id, lens_model) in [
        (rokinon_manufacturer.manufacturer_id, 'FE75MFT-B'),
        (canon_manufacturer.manufacturer_id, 'EF 17-40mm f/4L')
    ]]
except Exception as err: # pylint: disable=broad-except
    print('Create lens exception:', err)


if __name__ == '__main__':
    sys.exit(0)
