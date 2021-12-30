import { useState } from 'react'
import Button from 'components/Button'
import CameraFields from 'components/CameraFields'
import Input from 'components/Input'
import Label from 'components/Label'
import LensFields from 'components/LensFields'

const noop = () => {}

const numberOrNull = value => value !== '' ? Number(value) : null

const PhotoFields = ({
  photo,
  setter = noop,
  onSubmit,
  manufacturers = [],
  fileSupport = {},
}) => {
  const [handle, setHandle] = useState('')
  const [showDetails, setShowDetails] = useState(false)
  const [showCamera, setShowCamera] = useState(false)
  const [showLens, setShowLens] = useState(false)
  return (
    <>
      <h2>New Photo</h2>

      <Input
        label="Account"
        required
        type="text"
        name="account_handle"
        value={handle}
        onChange={e => setHandle(e.currentTarget.value)}
      />

      <Input
        label="Title"
        type="text"
        name="title"
        value={photo.photo_title}
        onChange={e => setter({ photo_title: e.currentTarget.value })}
      />

      <Input
        label="Description"
        type="text"
        name="description"
        value={photo.photo_text}
        onChange={e => setter({ photo_text: e.currentTarget.value })}
      />

      <Input
        label="Upload raw file"
        type="file"
        name="raw_file"
        onChange={e => setter({ raw_file: Array.from(e.currentTarget.files)[0] })}
        accept={fileSupport.raw_file?.map(ext => `.${ext}`)}
      />

      <Input
        label="Upload preview image"
        type="file"
        name="preview_file"
        onChange={e => setter({ preview_file: Array.from(e.currentTarget.files)[0] })}
        accept={fileSupport.preview_file?.map(ext => `.${ext}`)}
      />

      <Button onClick={() => setShowDetails(!showDetails)}>
        {!showDetails ? 'Show more' : 'Show less'}
      </Button>

      {showDetails && (
        <div className="card">
          <Input
            label="F-Stop"
            type="number"
            value={photo.aperture ?? undefined}
            min={0}
            onChange={e => setter({ aperture: numberOrNull(e.currentTarget.value) })}
          />

          <Input
            label="Flash"
            type="checkbox"
            value={!!photo.flash}
            onChange={e => setter({ flash: e.currentTarget.checked })}
          />

          <Input
            label="Focal length"
            type="number"
            value={photo.focal_length ?? undefined}
            min={0}
            onChange={e => setter({ focal_length: numberOrNull(e.currentTarget.value) })}
          />

          <Input
            label="ISO"
            type="number"
            value={photo.iso ?? undefined}
            min={0}
            onChange={e => setter({ iso: numberOrNull(e.currentTarget.value) })}
          />

          <div>
            <Input
              label="Shutter speed"
              type="number"
              value={photo.shutter_speed_denominator ?? undefined}
              min={0}
              onChange={e => setter({ shutter_speed_denominator: numberOrNull(e.currentTarget.value) })}
            />
            &nbsp;/&nbsp;
            <Input
              type="number"
              value={photo.shutter_speed_numerator ?? undefined}
              min={0}
              onChange={e => setter({ shutter_speed_numerator: numberOrNull(e.currentTarget.value) })}
            />
          </div>
        </div>
      )}

      {!showCamera && <Input label="Select camera body" />}

      {showCamera && (
        <div className="card">
          <CameraFields
            manufacturers={manufacturers}
            fields={photo}
            setter={setter}
          />
          <LensFields
            manufacturers={manufacturers}
            fields={photo}
            setter={setter}
          />
        </div>
      )}

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
        {!showCamera ? 'Add camera body or lens' : 'Remove camera body or lens'}
      </Button>

      {typeof onSubmit === 'function' && (
        <Button type="submit">Submit</Button>
      )}
    </>
  )
}

export default PhotoFields
