/**
 * Photo submission page
 */

import { useState } from 'react'
import { useRouter } from 'next/router'
import { id } from 'utils'
import { submitPhoto, submitEdit } from 'api'
import Button from 'components/Button'
import Input from 'components/Input'
import PhotoFields from 'components/PhotoFields'
import EditFields from 'components/EditFields'

const noop = () => {}

export const getStaticProps = async context => {
  try {
    const { fetchManufacturers, fetchFileSupport } = require('api')
    const mfrs = await fetchManufacturers()
    const fileSupport = await fetchFileSupport()
    return {
      props: {
        manufacturers: mfrs.data.manufacturers,
        fileSupport: fileSupport,
      },
      revalidate: 60,
    }
  } catch (err) {
    // console.warn('Caught error fetching manufacturers:\n', err)
  }
  return {
    props: {},
    revalidate: 5,
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

const photoFormState = () => ({
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

const editFormState = () => ({
  temp_id: id(),
  ...EditFields.inputs
})

const photoFormIsComplete = photo =>
  // input is not nullish
  photo &&
  // must have title or description
  (photo.photo_title?.length > 0 || photo.photo_text?.length > 0) &&
  // must include at least one file
  photo.preview_file !== photo.raw_file

const editFormIsComplete = edit =>
  // input is not nullish
  edit &&
  // must have title or description
  (edit.edit_title?.length > 0 || edit.edit_text?.length > 0) &&
  // must include at least one file
  edit.preview_file !== edit.edit_file

const CreatePhoto = ({ manufacturers = [], fileSupport = {} }) => {
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
    submitPhoto({ ...photo, account_handle: handle })
      .then(async ({ photoId }) => {
        if (photoId) {
          await Promise.all(edits.map(
            edit => submitEdit({
              ...edit,
              account_handle: handle,
              photo_id: photoId,
            }).then(noop, noop)
          ))
        }
        router.push(`/a/${encodeURIComponent(handle)}/p/${encodeURIComponent(photoId)}`)
      })
      .catch(err => {
        console.warn('Caught error while submitting photo:\n', err)
      })
  }

  return (
    <main>
      <form onSubmit={onSubmit}>
        <PhotoFields
          photo={photo}
          setter={fields => setPhoto(p => ({ ...p, ...fields }))}
          manufacturers={manufacturers}
          fileSupport={fileSupport}
        />
        <ul className="flex-row">
          {edits.map((edit, index) => (
            <li key={edit.temp_id} className="card">
              <Button
                title="Delete edit"
                appearance="link"
                className="close-btn"
                onClick={() => deleteEdit(index)}
              >
                &times;
              </Button>
              <EditFields
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
      </form>
    </main>
  )
}

export default CreatePhoto
