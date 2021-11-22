import styles from '../styles/Button.module.css'

const Button = ({ children, className = '', type = 'button', ...props }) => (
  <button type={type} className={`${styles.btn} ${className}`} {...props}>
    {children}
  </button>
)

export default Button
