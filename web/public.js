import { API_BASE } from 'config'
import { fetchWithTimeout } from 'utils'

/**
 * External APIs that require auth
 *
 * Use these functions clientside by passing the user's email and token as
 * basic authorization headers.
 */

const fetchWithAuth = ({ email, token }, endpoint, params) =>
  fetchWithTimeout(auth, endpoint, {
    ...params,
    headers: {
      ...(params.headers ?? {}),
      Authorization: `Basic ${btoa(`${email}:${token}`)}`
    },
  })

export const createAccount = (auth, { name, handle, token }) =>
  fetchWithAuth(auth, `${FLASK_BASE}/api/account`, {
    asJSON: false,
    body: JSON.stringify({ name, handle, token }),
    method: 'POST',
  })


export const submitPhoto = (auth, { raw_file, preview_file, ...photoForm }) => {
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
  return fetchWithAuth(auth, `${API_BASE}/photo`, {
    asJSON: false,
    body: formData,
    method: 'PUT',
  })
}

export const submitEdit = (auth, { edit_file, preview_file, ...editForm }) => {
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
  return fetchWithAuth(auth, `${API_BASE}/edit`, {
    asJSON: false,
    body: formData,
    method: 'PUT',
  })
}

export const submitReply = (auth, replyForm) => {}

export const submitReaction = (auth, reactionForm) => {}
