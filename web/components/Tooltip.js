import { useMemo } from 'react'
import { id as genID } from 'utils'
import styles from 'styles/Tooltip.module.css'

const Tooltip = ({ className, children, message = '' }) => {
  const id = useMemo(genID, [])
  return (
    <div className={styles.tooltip}>
      <input
        type="checkbox"
        className={styles.hiddenInput}
        id={`${id}-info`}
        onBlur={e => {
          e.currentTarget.checked = false
        }}
      />
      <label htmlFor={`${id}-info`} className={styles.infoLabel}>
        {children}
      </label>
      <div className={styles.body}>
        {message}
      </div>
    </div>
  )
}

export default Tooltip
