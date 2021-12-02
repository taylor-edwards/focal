const Image = ({ alt = '', src, srcFile, height, width, ...props }) => (
  <img
    {...props}
    alt={alt}
    src={src ?? srcFile?.path?.replace(/^.+(\/uploads\/[A-z0-9]+\.\w+)$/, '$1')}
    width={width ?? srcFile?.width}
    height={height ?? srcFile?.height}
  />)

export default Image
