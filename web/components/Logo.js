import Image from 'components/Image'
import styles from 'styles/Logo.module.css'

const Logo = ({ className = '', includeSubtext = false, size = 150 }) => (
  <Image
    src={`/focal${includeSubtext ? '-pics' : ''}.svg`}
    width={size * 2}
    height={size}
    style={{
      maxWidth: `${size * 2}px`,
    }}
    alt="Focal logo"
    className={`${styles.logo} ${className}`}
  />
)

export default Logo
