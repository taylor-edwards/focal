import NextLink from 'next/link'

const Link = ({ children, className, style, ...props }) => (
  <NextLink passHref {...props}>
    <a className={className} style={style}>{children}</a>
  </NextLink>
)

export default Link
