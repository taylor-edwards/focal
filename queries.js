/**
* Next endpoints:
*
* +-------------------+----------------+---------+
* | PUBLIC PATH       | FLASK PATH     | METHOD  |
* +-------------------+----------------+---------+
* | /api/create       | /account       | PUT     |
* |                   | /photo         | PUT     |
* |                   | /edit          | PUT     |
* |                   | /reply         | PUT     |
* |                   | /upvote        | PUT     |
* |                   | /preview       | PUT     |
* |                   | /tag           | PUT     |
* |                   | /editor        | PUT     |
* |                   | /camera        | PUT     |
* |                   | /lens          | PUT     |
* |                   | /manufacturer  | PUT     |
* | /api/update       | /account       | POST    |
* |                   | /photo         | POST    |
* |                   | /edit          | POST    |
* |                   | /reply         | POST    |
* |                   | /upvote        | POST    |
* |                   | /preview       | POST    |
* |                   | /tag           | POST    |
* |                   | /editor        | POST    |
* |                   | /camera        | POST    |
* |                   | /lens          | POST    |
* |                   | /manufacturer  | POST    |
* | /api/delete       | /account       | DELETE  |
* |                   | /photo         | DELETE  |
* |                   | /edit          | DELETE  |
* |                   | /reply         | DELETE  |
* |                   | /upvote        | DELETE  |
* |                   | /preview       | DELETE  |
* |                   | /tag           | DELETE  |
* |                   | /editor        | DELETE  |
* |                   | /camera        | DELETE  |
* |                   | /lens          | DELETE  |
* |                   | /manufacturer  | DELETE  |
* | /api/login        | /session       | POST    |
* | /api/logout       | /session       | DELETE  |
* | /                 | /graphql       | POST    |
* | /a/:user_name     | /graphql       | POST    |
* | /p/:photo_id      | /graphql       | POST    |
* | /e/:edit_id       | /graphql       | POST    |
* +-------------------+----------------+---------+
*
* USER    = An authenticated account session
* VISITOR = An anonymous guest without a session
*
* / is the landing page
*     /                                    Show marketing page to visitors
*     /                                    Redirect to /p or /e by account preference for users
*     /login/:token                        Authenticate user and set session cookie
*     /login                               Redirect to /
*     /logout                              Remove session cookie
* /a stands for Account.
*     /a                                   Show login/create account page to visitors
*     /a                                   Redirect to the user's account page (/a/:user_name)
*     /a/:user_name                        Show the account page for that user
* /p stands for Photo.
*     /p                                   Show global feed of photos to visitors
*     /p                                   Show photo feed from accounts the user follows
*     /p/:photo_id                         Show the photo page
*     /p/:photo_id/e/:edit_id              Show a specific edit for a photo
*     /p/:photo_id/e/:reply_id             Show a specific reply to a photo
*     /p/:photo_id/e/:edit_id/r/:reply_id  Show a specific reply to an edit for a photo
* /e stands for Edit.
*     /e                                   Show feed of edits
*     /e/:edit_id                          Show the edit page
*     /e/:edit_id/r/:reply_id              Show a specific reply to an edit
* /c stands for Create.
*     /c                                   Show photo posting page
*     /p/:photo_id/c                       Show edit posting page
*
* Complex UI templates can be cached in Next.
**/

const createAccount = (name, email) => fetch('http://localhost:5000/account', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    account_name: name,
    account_email: email,
  })
})

const editAccount = (id, options) => fetch(`http://localhost:5000/account/${id}`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(options)
})

const deleteAccount = id => fetch(`http://localhost:5000/account/${id}`, {
  method: 'DELETE',
})

deleteAccount(118)
.finally(() => createAccount('winnie', 'winnie@focal.pics'))
.finally(() => editAccount(119, { account_name: 'boobear', is_verified: true }))
