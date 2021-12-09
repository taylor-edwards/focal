import { useState } from 'react'
import Button from 'components/Button'
import Input from 'components/Input'
import Label from 'components/Label'

const noop = () => {}

const nullishOptionText = '---'

const valueOrNull = value => value === nullishOptionText ? null : value

const numberOrNull = value => value !== '' ? Number(value) : null

const LensForm = ({ fields, manufacturers, setter = noop }) => {
  const [showLensForm, setShowLensForm] = useState(false)
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
      {!showLensForm && <Input
        label="Select lens"
        type="select"
        value={fields.lens_id}
        onChange={selectLensModel}
        disabled={fields.lens_id === null && fields.lens_model !== ''}
      >
        {manufacturers
          .filter(({ id }) =>
            fields.lens_manufacturer_id === null || id === fields.lens_manufacturer_id
          )
          .map(({ lenses }) => lenses.map(
            ({ id, model }) => <option key={id} value={id}>{model}</option>
          ))}
      </Input>}

      {showLensForm && (
        <>
          <Input
            label="New lens name"
            type="text"
            value={fields.lens_model}
            onChange={e => setter({
              id: null,
              model: e.currentTarget.value,
            })}
          />
          <Input
            label="Select lens manufacturer"
            type="select"
            value={fields.lens_manufacturer_id ?? nullishOptionText}
            onChange={selectLensManufacturer}
            disabled={fields.lens_manufacturer_id === null &&
              fields.lens_manufacturer_name !== ''}
          >
            {manufacturers.map(({ id, name }) => (
              <option key={id} value={id}>{name}</option>
            ))}
          </Input>
          <Input
            label="Add manufacturer for lens"
            type="text"
            value={fields.lens_manufacturer_name}
            onChange={e => setter({
              manufacturer: {
                id: null,
                name: e.currentTarget.value,
              },
            })}
          />

          <div>
            <Input
              label="F-Stop range"
              type="number"
              value={fields.lens_aperture_min ?? ''}
              min={0}
              onChange={e => setter({
                aperture_min: numberOrNull(e.currentTarget.value),
              })}
            />
            &nbsp;&ndash;&nbsp;
            <Input
              type="number"
              value={fields.lens_aperture_max ?? ''}
              min={0}
              onChange={e => setter({
                aperture_max: numberOrNull(e.currentTarget.value),
              })}
            />
          </div>

          <div>
            <Input
              label="Focal length (mm)"
              type="number"
              value={fields.lens_focal_length_min ?? ''}
              min={0}
              onChange={e => setter({
                focal_length_min: numberOrNull(e.currentTarget.value),
              })}
            />
            &nbsp;/&nbsp;
            <Input
              type="number"
              value={fields.lens_focal_length_max ?? ''}
              min={0}
              onChange={e => setter({
                focal_length_max: numberOrNull(e.currentTarget.value),
              })}
            />
          </div>
        </>
      )}

      <Button onClick={() => setShowLensForm(!showLensForm)}>
        {showLensForm ? 'Remove lens' : 'Add lens'}
      </Button>
    </>
  )
}

export default LensForm
