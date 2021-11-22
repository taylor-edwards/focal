import { useState } from 'react'

const noop = () => {}

const nullishOption = '---'

const valueOrNull = value => value === nullishOption ? null : value

const numberOrNull = value => value !== '' ? Number(value) : null

const LensForm = ({ fields, manufacturers, setter = noop }) => {
  const selectLensManufacturer = e => setter({
    lens_manufacturer_id: valueOrNull(e.currentTarget.value),
    lens_manufacturer_name: '',
  })
  const selectLensModel = e => {
    const lens_id = valueOrNull(e.currentTarget.value)
    if (lens_id === null) {
      setter({ lens_id, model: '' })
    } else {
      const mfr = manufacturers.find(
        mfr => mfr.lenses.find(l => l.lens_id === lens_id),
      )
      setter({
        lens_id,
        lens_model: '',
        lens_aperture_min: null,
        lens_aperture_max: null,
        lens_focal_length_min: null,
        lens_focal_length_max: null,
        lens_manufacturer_id: mfr?.id ?? null,
        lens_manufacturer_name: mfr?.id ? '' : mfr?.name ?? '',
      })
    }
  }
  return (
    <>
      <div>
        <p>Lens manufacturer</p>
        <select
          value={fields.lens_manufacturer_id ?? nullishOption}
          onChange={selectLensManufacturer}
          disabled={fields.lens_manufacturer_id === null &&
            fields.lens_manufacturer_name !== ''}
        >
          <option value={null}>{nullishOption}</option>
          {manufacturers.map(({ id, name }) => (
            <option key={id} value={id}>{name}</option>
          ))}
        </select>
        <input
          type="text"
          value={fields.lens_manufacturer_name}
          onChange={e => setter({
            manufacturer: {
              id: null,
              name: e.currentTarget.value,
            },
          })}
        />
      </div>

      <div>
        <p>Lens model</p>
        <select
          value={fields.lens_id ?? nullishOption}
          onChange={selectLensModel}
          disabled={fields.lens_id === null && fields.lens_model !== ''}
        >
          <option value={null}>{nullishOption}</option>
          {manufacturers
            .filter(({ id }) =>
              fields.lens_manufacturer_id === null || id === fields.lens_manufacturer_id
            )
            .map(({ lenses }) => lenses.map(
              ({ id, model }) => <option key={id} value={id}>{model}</option>
            ))}
        </select>
        <input
          type="text"
          value={fields.lens_model}
          onChange={e => setter({
            id: null,
            model: e.currentTarget.value,
          })}
        />
        {fields.lens_id === null && <>
          <br />
          <label>
            <p>F-Stop range</p>
            <input
              type="number"
              value={fields.lens_aperture_min ?? ''}
              min={0}
              onChange={e => setter({
                aperture_min: numberOrNull(e.currentTarget.value),
              })}
            />
          </label>
          <label>
            &nbsp;&ndash;&nbsp;
            <input
              type="number"
              value={fields.lens_aperture_max ?? ''}
              min={0}
              onChange={e => setter({
                aperture_max: numberOrNull(e.currentTarget.value),
              })}
            />
          </label>
          <label>
            <p>Focal length (mm)</p>
            <input
              type="number"
              value={fields.lens_focal_length_min ?? ''}
              min={0}
              onChange={e => setter({
                focal_length_min: numberOrNull(e.currentTarget.value),
              })}
            />
          </label>
          <label>
            &nbsp;/&nbsp;
            <input
              type="number"
              value={fields.lens_focal_length_max ?? ''}
              min={0}
              onChange={e => setter({
                focal_length_max: numberOrNull(e.currentTarget.value),
              })}
            />
          </label>
        </>}
      </div>
    </>
  )
}

export default LensForm
