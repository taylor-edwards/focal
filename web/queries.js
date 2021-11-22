import { FLASK_ENDPOINT } from 'config'

export const fetchQuery = (name, query, variables = {}) => {
  const controller = new AbortController()
  const timer = setTimeout(
    () => controller.abort(),
    FLASK_ENDPOINT.DEFAULT_TIMEOUT,
  )
  return fetch(
    `${FLASK_ENDPOINT.BASE}/graphql`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        operationName: name,
        query: query,
        variables: variables,
      }),
      signal: controller.signal,
    }
  ).finally(() => {
    clearTimeout(timer)
  })
}

const previewFragment = `
  preview {
    filePath: previewFilePath
    width: previewWidth
    height: previewHeight
  }`

const photosFeedFragment = `
  photos {
    id: photoId
    title: photoTitle
    createdAt
    account {
      name: accountName
    }
    ${previewFragment}
  }
`

const editsFragment = `
  edits {
    id: editId
    title: editTitle
    filePath: editFilePath
    fileExtension: editFileExtension
    fileSize: editFileSize
    width: editWidth
    height: editHeight
    createdAt
    account {
      name: accountName
    }
    ${previewFragment}
  }
`

export const fetchAccounts = () => fetchQuery(
  'Accounts',
  `query Accounts {
    accounts {
      accountName
    }
  }`
)

export const fetchPublicAccount = ({ accountId, accountName }) => fetchQuery(
  'PublicAccount',
  `query PublicAccount($accountId: ID, $accountName: String) {
    account(accountId: $accountId, accountName: $accountName) {
      name: accountName
      createdAt
      editedAt
      ${photosFeedFragment}
      ${editsFragment}
    }
  }`,
  { accountId, accountName },
)

export const fetchPrivateAccount = ({ accountId, accountName }) => fetchQuery(
  'PrivateAccount',
  `query PrivateAccount($accountId: ID, $accountName: String) {
    account(accountId: $accountId, accountName: $accountName) {
      name: accountName
      email: accountEmail
      createdAt
      verifiedAt
      editedAt
      ${photosFeedFragment}
      ${editsFragment}
      bans {
        at: bannedAt
        until: bannedUntil
        reason: banReason
      }
      notifications {
        id: notificationId
        reason: notifyReason
        actor {
          name: accountName
        }
        photo: targetPhoto {
          id: photoId
          title: photoTitle
          ${previewFragment}
        }
        edit: targetEdit {
          id: editId
          title: editTitle
          ${previewFragment}
        }
      }
    }
  }`,
  { accountId, accountName },
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

export const fetchPhoto = photoId => fetchQuery(
  'Photo',
  `query Photo($photoId: ID!) {
    photo(photoId: $photoId) {
      id: photoId
      title: photoTitle
      description: photoDescription
      rawFilePath
      rawFileSize
      rawFileName
      rawFileExtension
      aperture
      focalLength
      iso
      shutterSpeedDenominator
      shutterSpeedNumerator
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
    }
  }`,
  { photoId },
)

export const fetchEdit = editId => fetchQuery(
  'Edit',
  `query Edit($editId: ID!) {
    id: editId
    title: editTitle
    description: editDescription
    filePath: editFilePath
    fileExtension: editFileExtension
    fileSize: editFileSize
    width: editWidth
    height: editHeight
    createdAt
    editedAt
    editor {
      id: editorId
      name: editorName
      version: editorVersion
      platform: editorPlatform
    }
  }`,
  { editId },
)
