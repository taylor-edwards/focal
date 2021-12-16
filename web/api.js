import { fetchWithTimeout } from 'utils'

export const fetchFileSupport = () => fetchWithTimeout('/api/file_support')

export const createAccount = ({ account_name, account_email }) =>
  fetchWithTimeout('/api/account', {
    body: JSON.stringify({ account_name, account_email }),
    method: 'POST',
  })

export const requestMagicLink = () => {}

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
  return fetchWithTimeout('/api/photo', {
    body: formData,
    method: 'PUT',
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
  return fetchWithTimeout('/api/edit', {
    body: formData,
    method: 'PUT',
  })
}

export const submitReply = () => {}

export const submitReaction = () => {}

export const fetchQuery = (name, query, variables = {}) => {
  const { FLASK_BASE } = require('config')
  return fetchWithTimeout(`${FLASK_BASE}/graphql`, {
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
  safename: accountSafename`

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

export const fetchAccount = ({ accountSafename }) => fetchQuery(
  'PublicAccount',
  `query PublicAccount($accountSafename: String) {
    account(accountSafename: $accountSafename) {
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
  { accountSafename },
)

export const fetchAccountDetails = ({ accountSafename }) => fetchQuery(
  'PrivateAccount',
  `query PrivateAccount($accountSafename: String) {
    account(accountSafename: $accountSafename) {
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
