import { FLASK_ENDPOINT } from 'config'

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
      name: accountName
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
      name: accountName
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
      name: accountName
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
      name: accountName
    }
  }`

const commonReplyFields = `
  id: replyId
  text: replyText
  createdAt
  editedAt`

const commonAccountFields = `
  name: accountName
  createdAt
  replies {
    ${commonReplyFields}
    photo {
      photoId
      photoTitle
      account {
        name: accountName
      }
    }
    edit {
      editId
      editTitle
      account {
        name: accountName
      }
    }
  }`

export const fetchAccounts = () => fetchQuery(
  'Accounts',
  `query Accounts {
    accounts {
      name: accountName
    }
  }`
)

export const fetchAccount = ({ accountName }) => fetchQuery(
  'PublicAccount',
  `query PublicAccount($accountName: String) {
    account(accountName: $accountName) {
      ${commonAccountFields}
      following {
        name: accountName
      }
      followers {
        name: accountName
      }
      photos {
        ${commonPhotoFields}
      }
      edits {
        ${commonEditFields}
      }
    }
  }`,
  { accountName },
)

export const fetchAccountDetails = ({ accountName }) => fetchQuery(
  'PrivateAccount',
  `query PrivateAccount($accountName: String) {
    account(accountName: $accountName) {
      name: accountName
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
            name: accountName
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
        name: accountName
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
        name: accountName
      }
      edits {
        title: editTitle
        previewFile {
          ${previewFields}
        }
        account {
          name: accountName
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
        name: accountName
      }
    }
  }`,
  { editId },
)
