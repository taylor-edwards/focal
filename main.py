import sys
from db import Database

db = Database('postgresql+psycopg2://albumator:asdf@127.0.0.1:5432/albumator')
print(f"Added users {db.insert_users(['chumpy', 'skeletor', 'nacho', 'jojo'])}")
print(f"All users: {[user.user_name for user in db.select_all_users()]}")
print(f"Added albums {db.insert_albums(['Landscape photos', 'Portraits'], 142)}")
print(f"Added photo {db.insert_photo('Mt Akina', 142, 223, '/path/to/preview.jpg', '/path/to/some/file.raw')}")
print(f"Added edit {db.insert_edit('Mt Akina remix', 142, 302, '/path/to/preview2.jpg', '/path/to/some/file2.xml')}")
print(f"A user's albums: {[album.album_name for album in db.select_user_albums(142)]}")
print(f"A user's photos: {[photo.photo_name for photo in db.select_user_photos(142)]}")
print(f"A photo's edits: {[edit.edit_name for edit in db.select_photo_edits(302)]}")

if __name__ == '__main__':
  sys.exit(0)
