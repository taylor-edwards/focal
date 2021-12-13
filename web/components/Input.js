import { useMemo } from 'react'
import { id } from 'utils'
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
  const inputId = useMemo(() => id(), []);
  const reverseLabelOrder = ['checkbox', 'radio'].includes(type);
  const labelElement = !label ? null : (
    <div className={styles.inputLabel}>
      <Label
        htmlFor={inputId}
        className={labelClassName}
      >
        {label}
      </Label>
      {info && (
        <div className={styles.info}>
          <input
            type="checkbox"
            className={styles.hiddenInput}
            id={`${inputId}-info`}
            onBlur={e => {
              e.currentTarget.checked = false
            }}
          />
          <label htmlFor={`${inputId}-info`} className={styles.infoLabel}>
            <span className="info-icon" role="none">i</span>
            <p className="aria-only">Show more info</p>
          </label>
          <p className={styles.infoBody}>{info}</p>
        </div>
      )}
    </div>
  );
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
  );
};

export default Input;
