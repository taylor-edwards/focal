import { useState } from 'react'
import Button from 'components/Button'
import CameraFields from 'components/CameraFields'
import LensFields from 'components/LensFields'

const noop = () => {}

const numberOrNull = value => value !== '' ? Number(value) : null

const PhotoForm = ({
  className,
  photo,
  setter = noop,
  onSubmit,
  manufacturers,
  fileSupport,
}) => {
  const [showDetails, setShowDetails] = useState(false)
  const [showCamera, setShowCamera] = useState(false)
  const [showLens, setShowLens] = useState(false)
  return (
    <form onSubmit={onSubmit}>
      <h2>Submit Photo</h2>

      <label>
        <p>Title</p>
        <input
          type="text"
          name="title"
          value={photo.photo_title}
          onChange={e => setter({ photo_title: e.currentTarget.value })}
        />
      </label>

      <label>
        <p>Description</p>
        <input
          type="text"
          name="description"
          value={photo.photo_description}
          onChange={e => setter({ photo_description: e.currentTarget.value })}
        />
      </label>

      <Button onClick={() => setShowDetails(!showDetails)}>
        {!showDetails ? 'Show more' : 'Show less'}
      </Button>

      {showDetails && (
        <>
          <label>
            <p>F-Stop</p>
            <input
              type="number"
              value={photo.aperture ?? undefined}
              min={0}
              onChange={e => setter({ aperture: numberOrNull(e.currentTarget.value) })}
            />
          </label>

          <label>
            <p>
              <input
                type="checkbox"
                value={!!photo.flash}
                onChange={e => setter({ flash: e.currentTarget.checked })}
              />
              Flash
            </p>
          </label>

          <label>
            <p>Focal length</p>
            <input
              type="number"
              value={photo.focal_length ?? undefined}
              min={0}
              onChange={e => setter({ focal_length: numberOrNull(e.currentTarget.value) })}
            />
          </label>

          <label>
            <p>ISO</p>
            <input
              type="number"
              value={photo.iso ?? undefined}
              min={0}
              onChange={e => setter({ iso: numberOrNull(e.currentTarget.value) })}
            />
          </label>

          <label>
            <p>Shutter speed</p>
            <input
              type="number"
              value={photo.shutter_speed_denominator ?? undefined}
              min={0}
              onChange={e => setter({ shutter_speed_denominator: numberOrNull(e.currentTarget.value) })}
            />
          </label>
          <label>
            &nbsp;/&nbsp;
            <input
              type="number"
              value={photo.shutter_speed_numerator ?? undefined}
              min={0}
              onChange={e => setter({ shutter_speed_numerator: numberOrNull(e.currentTarget.value) })}
            />
          </label>
        </>
      )}

      <label>
        <p>Upload raw file</p>
        <input
          type="file"
          name="raw_file"
          onChange={e => setter({ raw_file: Array.from(e.currentTarget.files)[0] })}
          accept={fileSupport.raw_file.map(ext => `.${ext}`)}
        />
      </label>

      <label>
        <p>Upload preview image</p>
        <input
          type="file"
          name="preview_file"
          onChange={e => setter({ preview_file: Array.from(e.currentTarget.files)[0] })}
          accept={fileSupport.preview_file.map(ext => `.${ext}`)}
        />
      </label>

      <Button onClick={() => {
        setShowCamera(!showCamera)
        // same as cameraFormState from pages/c.js
        setter({
          camera_id: null,
          camera_model: '',
          camera_manufacturer_id: null,
          camera_manufacturer_name: '',
        })
      }}>
        {!showCamera ? 'Add camera body' : 'Remove camera body'}
      </Button>

      {showCamera && (
        <CameraFields
          manufacturers={manufacturers}
          fields={photo}
          setter={setter}
        />
      )}

      <Button onClick={() => {
        setShowLens(!showLens)
        // same as lensFormState from pages/c.js
        setter({
          lens_id: null,
          lens_model: '',
          lens_aperture_min: null,
          lens_aperture_max: null,
          lens_focal_length_min: null,
          lens_focal_length_max: null,
          lens_manufacturer_id: null,
          lens_manufacturer_name: '',
        })
      }}>
        {!showLens ? 'Add camera lens' : 'Remove camera lens'}
      </Button>

      {showLens && (
        <LensFields
          manufacturers={manufacturers}
          fields={photo}
          setter={setter}
        />
      )}

      {typeof onSubmit === 'function' && (
        <Button type="submit">Submit</Button>
      )}
    </form>
  )
}

export default PhotoForm
