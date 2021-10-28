User A registers and has a default album created for them
User A uploads photos to their default album
User A creates an album
User A moves photos from default to custom album

User A adds User B to the album's editors list
User B creates an edit for one of User A's photos

User A
* Default album
* Custom album (owner)

User B
* Default album
* Custom album (editor)

User A Default Album
* Photos (contains all uploaded photos)

User B Default Album
* Photos (empty)

Custom album
* Owner: User A
* Editors: User B
* Photos

Photos
* Edits

Albums belong to Users
Photos belong to Users and Albums
Edits belong to Photos
Edits therefore must belong to the same Album as their parent Photo
