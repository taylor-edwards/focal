import { FLASK_ENDPOINT } from 'config'
import { createAbortController } from 'utils'

const toJSON = r => r.json()

/**
 * GraphQL endpoints should only be used in serverside code. They must not be
 * exposed to the internet because the GraphQL integration in this app does not
 * know how to authorize requests.
 *
 * Queries that need to be accessed from a client should be imported
 * dynamically in the getStaticPaths, getStaticProps and getServerSideProps
 * methods, or by proxy via an opaque REST endpoint in the corresponding
 * web/pages/api directory. Query consumers must perform request authorization
 * independently from this GraphQL integration.
 */

export const fetchQuery = (name, query, variables = {}) => {
  const controller = createAbortController()
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
  )
  .then(toJSON)
  .finally(() => {
    clearTimeout(timer)
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
