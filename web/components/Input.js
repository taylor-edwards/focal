import { useMemo } from 'react'
import { id } from 'utils'
import Tooltip from 'components/Tooltip'
import InfoIcon from 'components/InfoIcon'
import Label from 'components/Label'
import styles from 'styles/Input.module.css'

const nullishOptionText = '---'

const Input = ({
  className = '',
  children,
  labelClassName,
  type = 'text',
  label,
  info,
  value,
  suggestions = [], // pass manufacturer/camera body/lens model lists here
  ...props
}) => {
  const inputId = useMemo(() => id(), [])
  const reverseLabelOrder = ['checkbox', 'radio'].includes(type)
  const labelElement = !label ? null : (
    <div className={styles.inputLabel}>
      <Label htmlFor={inputId} className={labelClassName}>
        {label}
      </Label>
      {info && (
        <Tooltip message={info}>
          <InfoIcon />
        </Tooltip>
      )}
    </div>
  )
  return (
    <>
      {!reverseLabelOrder && labelElement}

      {type === 'select' ? (
        <select value={value ?? nullishOptionText} {...props}>
          <option value={null}>{nullishOptionText}</option>
          {children}
        </select>
      ) : (
        <input
          id={inputId}
          value={value}
          className={`${styles.input} ${className}`}
          type={type}
          {...props}
        />
        /* render suggestions here as a list of buttons */
      )}

      {reverseLabelOrder && labelElement}
    </>
  )
}

export default Input
