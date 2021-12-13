import { FLASK_ENDPOINT } from 'config'

const toJSON = r => r.json()

export const fetchFileSupport = () => fetch(
  `${FLASK_ENDPOINT.BASE}/config/supported_file_extensions`,
).then(toJSON)

export const createAccount = ({ account_name, account_email }) =>
  fetch(`${FLASK_ENDPOINT.BASE}/account`, {
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ account_name, account_email }),
    method: 'POST',
  }).then(toJSON)

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
  return fetch(`${FLASK_ENDPOINT.BASE}/photo`, {
    body: formData,
    method: 'PUT',
  }).then(toJSON)
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
  return fetch(`${FLASK_ENDPOINT.BASE}/edit`, {
    body: formData,
    method: 'PUT',
  }).then(toJSON)
}
