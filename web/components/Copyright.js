import { useMemo } from 'react'

const Copyright = ({ className = '' }) => {
  const year = useMemo(() => new Date().getFullYear(), [])
  return (
    <p className={`copyright ${className}`}>
      &copy; Copyright Focal Pics 2020&ndash;{year}
    </p>
  )
}

export default Copyright
