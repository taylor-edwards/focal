import styles from 'styles/Label.module.css'

const Label = ({ children, className = '', ...props }) => (
  <label className={`${styles.label} ${className}`} {...props}>
    {children}
  </label>
)

export default Label
