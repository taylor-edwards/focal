import NextLink from 'next/link'

const Link = ({
  children,
  className,
  download,
  file,
  href,
  style,
  target,
  title,
  ...props
}) => (
  <NextLink
    passHref
    {...props}
    href={href ?? file?.path?.replace(/^.+(\/uploads\/[A-z0-9]+\.\w+)$/, '$1')}
    legacyBehavior
  >
    <a
      className={className}
      style={style}
      download={download ?? file?.name}
      title={title ?? file?.name}
      target={target ?? (download || file) ? '_blank' : undefined}
    >{children}</a>
  </NextLink>
)

export default Link
