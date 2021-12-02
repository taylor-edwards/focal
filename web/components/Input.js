import { useMemo } from 'react'
import { id } from 'utils'
import Label from 'components/Label'

const Input = ({
  className = '',
  labelClassName,
  type = 'text',
  label,
  value,
  ...props
}) => {
  const inputId = useMemo(() => id(), [])
  return (
    <>
      {label && (
        <Label htmlFor={inputId} className={labelClassName}>
          {label}
        </Label>
      )}
      <input
        id={inputId}
        value={value}
        className={`input ${className}`}
        type={type}
        {...props}
      />
    </>
  )
}

export default Input
