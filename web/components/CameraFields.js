import { useState } from 'react'

const noop = () => {}

const nullishOption = '---'

const valueOrNull = value =>
  (value === nullishOption || value === '') ? null : value

// const stringOrNull = value =>
//   typeof value === 'string' && string.length > 0 ? value : null

const CameraFields = ({ fields, manufacturers, setter = noop }) => {
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
      <div>
        <p>Camera manufacturer</p>
        <select
          value={fields.camera_manufacturer_id ?? nullishOption}
          onChange={selectCameraManufacturer}
          disabled={fields.camera_manufacturer_id === null &&
            fields.camera_manufacturer_name !== ''}
        >
          <option value={null}>{nullishOption}</option>
          {manufacturers.map(({ id, name }) => (
            <option key={id} value={id}>{name}</option>
          ))}
        </select>
        <input
          type="text"
          value={fields.camera_manufacturer_name}
          onChange={e => setter({
            camera_manufacturer_id: null,
            camera_manufacturer_name: e.currentTarget.value,
          })}
        />
      </div>

      <div>
        <p>Camera body</p>
        <select
          value={fields.camera_id ?? nullishOption}
          onChange={selectCameraBody}
          disabled={fields.camera_id === null && fields.camera_model !== ''}
        >
          <option value={null}>{nullishOption}</option>
          {manufacturers
            .filter(({ id }) =>
              fields.camera_manufacturer_id === null || id === fields.camera_manufacturer_id
            )
            .map(({ cameras }) => cameras.map(
              ({ id, model }) => <option key={id} value={id}>{model}</option>
            ))}
        </select>
        <input
          type="text"
          value={fields.camera_model}
          onChange={e => setter({
            camera_id: null,
            camera_model: e.currentTarget.value,
          })}
        />
      </div>
    </>
  )
}

export default CameraFields
