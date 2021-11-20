/**
 * Photo submission page
 */

import { useState } from 'react'
import { PAGE_REVALIDATION_INTERVAL } from 'constants'

const noop = () => {}

export const getStaticProps = async context => {
  try {
    const { fetchManufacturers } = require('queries')
    const response = await fetchManufacturers()
    const json = await response.json()
    console.log(json)
    return {
      props: json.data,
      revalidate: PAGE_REVALIDATION_INTERVAL,
    }
  } catch (err) {
    console.warn('Caught error fetching equipment:', err)
  }
  return {
    notFound: true,
    revalidate: PAGE_REVALIDATION_INTERVAL,
  }
}

const PhotoForm = ({ className, photo = {}, setter = noop, manufacturers }) => {
  const [cameraMFId, setCameraMFId] = useState(null)
  const [lensMFId, setLensMFId] = useState(null)
  return (
    <form className={className}>
      <h1>Submit Photo</h1>
      <label>
        <p>Title</p>
        <input
          type="text"
          name="title"
          value={photo.photo_title}
          onInput={e => setter({ photo_title: e.currentTarget.value })}
        />
      </label>
      <label>
        <p>Description</p>
        <input type="text" name="description" />
      </label>
      <label>
        <p>Upload raw file</p>
        <input type="file" name="raw-file" />
      </label>
      <label>
        <p>Upload preview image</p>
        <input type="file" name="preview-file" />
      </label>

      <label>
        <p>Camera manufacturer</p>
        <select onChange={e => setCameraMFId(e.currentTarget.value)}>
          {manufacturers.map(({ id, name }) => (
            <option key={id} value={id}>{name}</option>
          ))}
        </select>
      </label>
      <label>
        <p>Camera model</p>
        <select>
          <option value={null}>---</option>
          {manufacturers.filter(({ id }) => id === cameraMFId).map(
            ({ cameras }) => cameras.map(
              ({ id, model }) => <option key={id} value={id}>{model}</option>
            )
          )}
        </select>
      </label>

      <label>
        <p>Lens manufacturer</p>
        <select onChange={e => setLensMFId(e.currentTarget.value)}>
          <option value={null}>---</option>
          {manufacturers.map(
            ({ id, name }) => <option key={id} value={id}>{name}</option>
          )}
        </select>
      </label>
      <label>
        <p>Lens model</p>
        <select>
          <option value={null}>---</option>
          {manufacturers.filter(({ id }) => id === lensMFId).map(
            ({ lenses }) => lenses.map(
              ({ id, model }) => <option key={id} value={id}>{model}</option>
            )
          )}
        </select>
      </label>
    </form>
  )
}

const EditForm = ({ className, edit = {}, setter = noop }) => (
  <form className={className}>
    <h1>Submit Edit</h1>
    <label>
      <p>Title</p>
      <input type="text" name="title" />
    </label>
    <label>
      <p>Description</p>
      <input type="text" name="description" />
    </label>
    <label>
      <p>Upload raw file</p>
      <input type="file" name="raw-file" />
    </label>
    <label>
      <p>Upload preview image</p>
      <input type="file" name="preview-file" />
    </label>
  </form>
)

const createPreview = () => ({
  preview_file_path: null,
  preview_file_size: null,
  preview_width: null,
  preview_height: null,
})

const createPhoto = () => ({
  photo_title: '',
  preview: null,
  camera_id: null,
  lens_id: null,
  photo_description: null,
  raw_file_path: null,
  raw_file_extension: null,
  raw_file_size: null,
  raw_width: null,
  raw_height: null,
  aperture: null,
  flash: null,
  focal_length: null,
  iso: null,
  shutter_speed_denominator: null,
  shutter_speed_numerator: null,
})

const createEdit = () => ({
  temp_id: Math.random().toString().substr(2),
  edit_title: '',
  preview_id: null,
  photo_id: null,
  editor_id: null,
  edit_description: null,
  edit_file_path: null,
  edit_file_extension: null,
  edit_file_size: null,
  edit_width: null,
  edit_height: null,
})

const CreatePhoto = ({ manufacturers }) => {
  const [photo, setPhoto] = useState(createPhoto())
  const [edits, setEdits] = useState([])
  const setEditForm = index => edit => setEdits(
    edits.slice(0, index).concat({
      ...edits[index],
      ...edit,
    }).concat(edits.slice(index + 1))
  )
  console.log(JSON.stringify(photo, null, 4))
  console.log(JSON.stringify(edits, null, 4))
  return (
    <div>
      <PhotoForm
        photo={photo}
        setPhoto={form => ({ ...photo, ...form })}
        manufacturers={manufacturers}
      />
      <ul>
        {edits.map((edit, index) => (
          <li key={edit.temp_id}>
            <button onClick={() => setEdits(
              edits.slice(0, index).concat(edits.slice(index + 1)),
            )}>&times; Delete edit</button>
            <EditForm edit={edit} setter={setEditForm(index)} />
          </li>
        ))}
      </ul>
      <button onClick={() => setEdits(edits.concat(createEdit()))}>
        + Add edit
      </button>
    </div>
  )
}

export default CreatePhoto
