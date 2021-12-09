import styles from 'styles/Button.module.css'

const Button = ({
  appearance = 'button',
  children,
  className = '',
  type = 'button',
  ...props
}) => (
  <button
    type={type}
    className={`${
        appearance === 'button' ? styles.btn : ''
      } ${
        appearance === 'link' ? styles.link : ''
      } ${className}`}
    {...props}
  >
    {children}
  </button>
)

export default Button
