import Image from 'components/Image'
import styles from 'styles/Logo.module.css'

const Logo = ({ className = '', includeSubtext = false }) => (
  <Image
    src={`/focal${includeSubtext ? '-pics' : ''}.svg`}
    width="300"
    height="150"
    alt="Focal logo"
    className={`${styles.logo} ${className}`}
  />
)

export default Logo
