/**
 * Photo submission page
 */

import { useState } from 'react'
import { useRouter } from 'next/router'
import { PAGE_REVALIDATION_INTERVAL } from 'config'
import { submitPhoto, submitEdit } from 'api'
import Button from 'components/Button'
import PhotoForm from 'components/PhotoForm'
import EditForm from 'components/EditForm'

const noop = () => {}

export const getStaticProps = async context => {
  try {
    const { fetchManufacturers } = require('queries')
    const { fetchFileSupport } = require('api')
    const mfrs = await fetchManufacturers()
      .then(r => r.json())
      .catch(err => console.error(err))
    const fileSupport = await fetchFileSupport()
      .then(r => r.json())
      .catch(err => console.error(err))
    return {
      props: {
        manufacturers: mfrs.data.manufacturers,
        fileSupport: fileSupport,
      },
      revalidate: PAGE_REVALIDATION_INTERVAL,
    }
  } catch (err) {
    console.warn('Caught error fetching manufacturers:', err)
  }
  return {
    notFound: true,
    revalidate: PAGE_REVALIDATION_INTERVAL,
  }
}

const cameraFormState = () => ({
  camera_id: null,
  camera_model: '',
  camera_manufacturer_id: null,
  camera_manufacturer_name: '',
})

const lensFormState = () => ({
  lens_id: null,
  lens_model: '',
  lens_aperture_min: null,
  lens_aperture_max: null,
  lens_focal_length_min: null,
  lens_focal_length_max: null,
  lens_manufacturer_id: null,
  lens_manufacturer_name: '',
  lens_filter: '',
})

const photoFormState = (account_name) => ({
  photo_title: '',
  photo_text: '',
  raw_file: null,
  preview_file: null,
  aperture: null,
  flash: null,
  focal_length: null,
  iso: null,
  shutter_speed_denominator: null,
  shutter_speed_numerator: null,
  ...cameraFormState(),
  ...lensFormState(),
})

const editFormState = (account_name) => ({
  temp_id: Math.random().toString(16).substr(2),
  edit_title: '',
  edit_text: '',
  edit_file: null,
  preview_file: null,
  editor_id: null,
  editor_name: '',
  editor_version: '',
  editor_platform: '',
})

const photoFormIsComplete = photo =>
  // input is not nullish
  photo &&
  // must have title or description
  (photo.photo_title?.length > 0 || photo.photo_text?.length > 0) &&
  // must include at least one file
  photo.preview_file != photo.raw_file

const editFormIsComplete = edit =>
  // input is not nullish
  edit &&
  // must have title or description
  (edit.edit_title?.length > 0 || edit.edit_text?.length > 0) &&
  // must include at least one file
  edit.preview_file != edit.edit_file

const CreatePhoto = ({ manufacturers = [], fileSupport = {} }) => {
  const [accountName, setAccountName] = useState('')
  const router = useRouter()
  const [photo, setPhoto] = useState(photoFormState())
  const [edits, setEdits] = useState([])

  const addEdit = () => {
    setEdits(e => e.concat(editFormState()))
  }

  const deleteEdit = index =>
    setEdits(e => e.slice(0, index).concat(e.slice(index + 1)))

  const setEdit = index => fields => setEdits(
    e => e.slice(0, index).concat({
      ...e[index],
      ...fields,
    }).concat(e.slice(index + 1))
  )

  const onSubmit = e => {
    e.preventDefault()
    e.stopPropagation()
    if (!photoFormIsComplete(photo)) {
      console.log('Photo form is incomplete!', photo, edits)
      return
    }
    const editFormsComplete = edits.reduce(
      (truthy, edit) => truthy ? editFormIsComplete(edit) : false,
      true,
    )
    if (!editFormsComplete) {
      console.log('Edit form is incomplete!', photo, edits)
      return
    }
    submitPhoto({ ...photo, account_name: accountName })
      .then(response => response.json())
      .then(async ({ photoId }) => {
        if (photoId) {
          await Promise.all(edits.map(
            edit => submitEdit({
              ...edit,
              account_name: accountName,
              photo_id: photoId,
            }).then(noop, noop)
          ))
        }
        router.push(`/a/${accountName}/p/${photoId}`)
      })
      .catch(err => {
        console.warn('Caught error while submitting photo', err)
      })
  }

  return (
    <main>
      <label>
        <p>Account</p>
        <input
          type="text"
          name="account_name"
          value={accountName}
          onChange={e => setAccountName(e.currentTarget.value)}
        />
      </label>
      <PhotoForm
        photo={photo}
        setter={fields => setPhoto(p => ({ ...p, ...fields }))}
        manufacturers={manufacturers}
        onSubmit={onSubmit}
        fileSupport={fileSupport}
      />
      <ul className="flex-row">
        {edits.map((edit, index) => (
          <li key={edit.temp_id}>
            <Button onClick={() => deleteEdit(index)}>&times; Delete edit</Button>
            <EditForm
              edit={edit}
              setter={setEdit(index)}
              fileSupport={fileSupport}
            />
          </li>
        ))}
      </ul>
      <Button onClick={addEdit}>
        + Add edit
      </Button>
    </main>
  )
}

export default CreatePhoto
