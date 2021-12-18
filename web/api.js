import { FLASK_BASE } from 'config'
import { fetchWithTimeout } from 'utils'

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
  fetchWithTimeout(`${FLASK_BASE}/config/file_support`)

export const createSession = account_email =>
  fetchWithTimeout(`${FLASK_BASE}/session`, {
    method: 'POST',
    body: JSON.stringify({ account_email }),
  })

export const verifySession = token =>
  fetchWithTimeout(`${FLASK_BASE}/session`, {
    method: 'POST',
    body: JSON.stringify({ token }),
  })

export const deleteSession = token =>
  fetchWithTimeout(`${FLASK_BASE}/session`, {
    method: 'DELETE',
    body: JSON.stringify({ token }),
  })

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
