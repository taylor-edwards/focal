import Image from 'components/Image'

const Logo = ({ className, includeSubtext = false }) => (
  <Image
    src={`/focal${includeSubtext ? '-pics' : ''}.svg`}
    width="300"
    height="150"
    alt="Focal logo"
    className={className}
  />
)

export default Logo
