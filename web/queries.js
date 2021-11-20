import { FLASK_ENDPOINT } from './constants'

export const fetchQuery = (name, query, variables={}) => {
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

const photosMiniFeed = `
  photos {
    id: photoId
    title: photoTitle
    createdAt
    account {
      name: accountName
    }
    preview {
      filePath: previewFilePath
    }
  }
`

const editsMiniFeed = `
  edits {
    id: editId
    title: editTitle
    createdAt
    account {
      name: accountName
    }
    preview {
      filePath: previewFilePath
    }
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

export const fetchPublicAccount = vars => fetchQuery(
  'PublicAccount',
  `query PublicAccount($accountId: ID, $accountName: String) {
    account(accountId: $accountId, accountName: $accountName) {
      name: accountName
      createdAt
      editedAt
      ${photosMiniFeed}
      ${editsMiniFeed}
    }
  }`,
  vars,
)

export const fetchPrivateAccount = vars => fetchQuery(
  'PrivateAccount',
  `query PrivateAccount($accountId: ID, $accountName: String) {
    account(accountId: $accountId, accountName: $accountName) {
      name: accountName
      email: accountEmail
      createdAt
      verifiedAt
      editedAt
      ${photosMiniFeed}
      ${editsMiniFeed}
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
          preview {
            filePath: previewFilePath
          }
        }
        edit: targetEdit {
          id: editId
          title: editTitle
          preview {
            filePath: previewFilePath
          }
        }
      }
    }
  }`,
  vars,
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
