import styles from 'styles/InfoIcon.module.css'

const InfoIcon = ({ className = '' }) => (
  <span
    className={`${styles.infoIcon} ${className}`}
    title="info"
  >
    i
  </span>
)

export default InfoIcon
