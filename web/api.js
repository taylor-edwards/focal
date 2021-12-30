import { PUBLIC_API, PRIVATE_API } from 'config'
import { fetchWithAuth, fetchWithTimeout } from 'utils'

/**
 * Public APIs for access from the web client in-browser
 *
 * These calls are authenticated by an HttpOnly cookie
 */

export const createAccount = ({ name, handle }) =>
  fetchWithTimeout(`${PUBLIC_API}/account`, {
    method: 'POST',
    body: JSON.stringify({ account_name: name, account_handle: handle }),
  })

export const submitPhoto = ({ raw_file, preview_file, ...photoForm }) => {
  const formData = new FormData()
  if (raw_file) {
    formData.append('raw_file', raw_file, raw_file.name)
  }
  if (preview_file) {
    formData.append('preview_file', preview_file, preview_file.name)
  }
  for (const key in photoForm) {
    formData.set(key, photoForm[key])
  }
  return fetchWithTimeout(`${PUBLIC_API}/photo`, {
    asJSON: false,
    method: 'PUT',
    body: formData,
  })
}

export const submitEdit = ({ edit_file, preview_file, ...editForm }) => {
  const formData = new FormData()
  if (edit_file) {
    formData.append('edit_file', edit_file, edit_file.name)
  }
  if (preview_file) {
    formData.append('preview_file', preview_file, preview_file.name)
  }
  for (const key in editForm) {
    formData.set(key, editForm[key])
  }
  return fetchWithTimeout(`${PUBLIC_API}/edit`, {
    asJSON: false,
    method: 'PUT',
    body: formData,
  })
}

export const submitReply = (reply) => {
  return fetchWithTimeout(`${PUBLIC_API}/reply`, {
    method: 'PUT',
    body: JSON.stringify({
      photo_id: reply.photoId,
      edit_id: reaction.editId,

    }),
  })
}

export const submitReaction = (reaction) => {
  return fetchWithTimeout(`${PUBLIC_API}/reaction`, {
    method: 'PUT',
    body: JSON.stringify({
      photo_id: reaction.photoId,
      edit_id: reaction.editId,
      reply_id: reaction.replyId,
      reaction_id: reaction.reactionId,
    }),
  })
}

/**
 * Internal APIs that can only be accessed from within the Docker network
 *
 * Use these functions serverside by importing them within the methods:
 *   - getServerSideProps
 *   - getStaticProps
 *   - getStaticPaths
 *
 * Example:
 * ```js
 * export const getStaticProps = async context => {
 *   try {
 *     const { fetchFileSupport } = require('api')
 *     const fileSupport = await fetchFileSupport()
 *     return { props: { fileSupport }, revalidate: 600 }
 *   } catch (err) {
 *     // do something with the error
 *   }
 *   return { props: {}, revalidate: 30 }
 * }
 * ```
 */

export const fetchFileSupport = () =>
  fetchWithTimeout(`${PRIVATE_API}/config/file_support`)

export const createSession = account_email =>
  fetchWithTimeout(`${PRIVATE_API}/session`, {
    method: 'PUT',
    body: JSON.stringify({ account_email }),
  })

export const authorizeSession = token =>
  fetchWithAuth(token, `${PRIVATE_API}/session`, {
    method: 'POST',
  })

export const deleteSession = token =>
  fetchWithAuth(token, `${PRIVATE_API}/session`, {
    asJSON: false,
    method: 'DELETE',
  })

export const getSession = token =>
  fetchWithAuth(token, `${PRIVATE_API}/session`).catch(err => ({}))

export const getAccountDetails = token =>
  fetchWithAuth(token, `${PRIVATE_API}/account`).catch(err => ({}))

/**
 * GraphQL clientside integration for serverside usage only
 */

const fetchQuery = (name, query, variables = {}) => {
  const { PRIVATE_API } = require('config')
  return fetchWithTimeout(`${PRIVATE_API}/graphql`, {
    method: 'POST',
    body: JSON.stringify({
      operationName: name,
      query: query,
      variables: variables,
    }),
  })
}

const accountNameFields = `
  name: accountName
  handle: accountHandle`

const previewFields = `
  path: filePath
  width: imageWidth
  height: imageHeight`


const fileFields = `
  name: fileName
  path: filePath
  ext: fileExtension
  size: fileSize`

const commonPhotoFields = `
  id: photoId
  title: photoTitle
  text: photoText
  createdAt
  editedAt
  previewFile {
    ${previewFields}
  }
  rawFile {
    ${fileFields}
    width: imageWidth
    height: imageHeight
  }
  edits {
    id: editId
    title: editTitle
    createdAt
    account {
      ${accountNameFields}
    }
    previewFile {
      ${previewFields}
    }
  }
  replies {
    id: replyId
    text: replyText
    createdAt
    account {
      ${accountNameFields}
    }
  }`

const commonEditFields = `
  id: editId
  title: editTitle
  text: editText
  createdAt
  editedAt
  previewFile {
    ${previewFields}
  }
  sidecarFile {
    ${fileFields}
  }
  photo {
    id: photoId
    title: photoTitle
    createdAt
    account {
      ${accountNameFields}
    }
    previewFile {
      ${previewFields}
    }
  }
  replies {
    id: replyId
    text: replyText
    createdAt
    account {
      ${accountNameFields}
    }
  }`

const commonReplyFields = `
  id: replyId
  text: replyText
  createdAt
  editedAt`

const commonAccountFields = `
  ${accountNameFields}
  createdAt
  replies {
    ${commonReplyFields}
    photo {
      photoId
      photoTitle
      account {
        ${accountNameFields}
      }
    }
    edit {
      editId
      editTitle
      account {
        ${accountNameFields}
      }
    }
  }`

export const fetchAccounts = () => fetchQuery(
  'Accounts',
  `query Accounts {
    accounts {
      ${accountNameFields}
    }
  }`
)

export const fetchAccount = ({ accountHandle }) => fetchQuery(
  'PublicAccount',
  `query PublicAccount($accountHandle: String) {
    account(accountHandle: $accountHandle) {
      ${commonAccountFields}
      following {
        ${accountNameFields}
      }
      followers {
        ${accountNameFields}
      }
      photos {
        ${commonPhotoFields}
      }
      edits {
        ${commonEditFields}
      }
    }
  }`,
  { accountHandle },
)

export const fetchAccountDetails = ({ accountEmail }) => fetchQuery(
  'PrivateAccount',
  `query PrivateAccount($accountEmail: String) {
    account(accountEmail: $accountEmail) {
      ${accountNameFields}
      email: accountEmail
      role: accountRole
      createdAt
      editedAt
      flags {
        id: flagId
        name: flagName
        text: flagText
      }
      bans {
        id: banId
        createdAt
        expiresAt
        name: banName
        text: banText
      }
      notifications {
        id: notificationId
        createdAt
        viewedAt
        event {
          account {
            ${accountNameFields}
          }
          photo {
            id: photoId
            title: photoTitle
          }
          edit {
            id: editId
            title: editTitle
          }
          reply {
            id: replyId
            text: replyText
          }
        }
      }
    }
  }`,
  { accountName },
)

export const fetchManufacturers = () => fetchQuery(
  'Manufacturers',
  `query Manufacturers {
    manufacturers {
      id: manufacturerId
      name: manufacturerName
      cameras {
        id: cameraId
        model: cameraModel
      }
      lenses {
        id: lensId
        model: lensModel
      }
    }
  }`
)

export const fetchPhotos = (options = {}) => fetchQuery(
  'Photos',
  `query Photos {
    photos {
      ${commonPhotoFields}
      account {
        ${accountNameFields}
        previewFile {
          ${previewFields}
        }
      }
    }
  }`,
  options,
)

export const fetchPhoto = photoId => fetchQuery(
  'Photo',
  `query Photo($photoId: ID!) {
    photo(photoId: $photoId) {
      ${commonPhotoFields}
      id: photoId
      title: photoTitle
      text: photoText
      aperture
      focalLength
      iso
      shutterSpeedDenominator
      shutterSpeedNumerator
      account {
        ${accountNameFields}
        previewFile {
          ${previewFields}
        }
      }
      previewFile {
        ${previewFields}
      }
      camera {
        id: cameraId
        model: cameraModel
        manufacturer {
          id: manufacturerId
          name: manufacturerName
        }
      }
      lens {
        id: lensId
        model: lensModel
        manufacturer {
          id: manufacturerId
          name: manufacturerName
        }
      }
      account {
        ${accountNameFields}
      }
      edits {
        title: editTitle
        previewFile {
          ${previewFields}
        }
        account {
          ${accountNameFields}
        }
      }
    }
  }`,
  { photoId },
)

export const fetchEdit = editId => fetchQuery(
  'Edit',
  `query Edit($editId: ID!) {
    edit(editId: $editID) {
      id: editId
      title: editTitle
      text: editText
      createdAt
      editedAt
      sidecarFile {
        ${fileFields}
      }
      previewFile {
        ${previewFields}
      }
      editor {
        id: editorId
        name: editorName
        version: editorVersion
        platform: editorPlatform
      }
      account {
        ${accountNameFields}
      }
    }
  }`,
  { editId },
)

export const fetchReactions = () => fetchQuery(
  'Reactions',
  `query Reactions() {
    reactions {
      name: reactionName
      emoji: reactionEmoji
    }
  }`,
)
