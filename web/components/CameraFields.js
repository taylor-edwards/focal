import { useState } from 'react'
import Button from 'components/Button'
import Input from 'components/Input'
import Label from 'components/Label'

const noop = () => {}

const nullishOption = '---'

const valueOrNull = value =>
  (value === nullishOption || value === '') ? null : value

// const stringOrNull = value =>
//   typeof value === 'string' && string.length > 0 ? value : null

const CameraFields = ({ fields, manufacturers, setter = noop }) => {
  const [showCameraForm, setShowCameraForm] = useState(false)
  const selectCameraManufacturer = e => setter({
    camera_manufacturer_id: valueOrNull(e.currentTarget.value),
    camera_manufacturer_name: '',
  })
  const selectCameraBody = e => {
    const camera_id = valueOrNull(e.currentTarget.value)
    if (camera_id === null) {
      setter({ camera_id, camera_model: '' })
    } else {
      const mfr = manufacturers.find(
        mfr => mfr.cameras.find(c => c.camera_id === camera_id),
      )
      setter({
        camera_id,
        camera_model: '',
        camera_manufacturer_id: mfr?.id ?? null,
        camera_manufacturer_name: mfr?.id ? '' : mfr?.name ?? '',
      })
    }
  }
  return (
    <>
      {!showCameraForm && <Input
        label="Select camera body"
        type="select"
        value={fields.camera_manufacturer_id}
        onChange={selectCameraManufacturer}
        disabled={fields.camera_manufacturer_id === null &&
          fields.camera_manufacturer_name !== ''}
      >
        {manufacturers.map(({ id, name }) => (
          <option key={id} value={id}>{name}</option>
        ))}
      </Input>}

      {showCameraForm && (
        <>
          <Input
            label="New camera name"
            type="text"
            value={fields.camera_model}
            onChange={e => setter({
              camera_id: null,
              camera_model: e.currentTarget.value,
            })}
          />

          <Input
            label="Select camera manufacturer"
            type="select"
            value={fields.camera_id}
            onChange={selectCameraBody}
            disabled={fields.camera_id === null && fields.camera_model !== ''}
          >
            {manufacturers
              .filter(({ id }) =>
                fields.camera_manufacturer_id === null || id === fields.camera_manufacturer_id
              )
              .map(({ cameras }) => cameras.map(
                ({ id, model }) => <option key={id} value={id}>{model}</option>
              ))}
          </Input>

          <Input
            label="Add manufacturer for camera body"
            type="text"
            value={fields.camera_manufacturer_name}
            onChange={e => setter({
              camera_manufacturer_id: null,
              camera_manufacturer_name: e.currentTarget.value,
            })}
          />
        </>
      )}

      <Button onClick={() => setShowCameraForm(!showCameraForm)}>
        {showCameraForm ? 'Remove camera body' : 'Add camera body'}
      </Button>
    </>
  )
}

export default CameraFields
