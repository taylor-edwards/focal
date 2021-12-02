import { useMemo } from 'react'

const DateTime = ({ date }) => {
  const timeString = useMemo(() => {
    const d = date instanceof Date ? date : new Date(date)
    if (new Date() - d < 43200000) {
      // if date is within 12 hours of posting, show just the time
      return d.toLocaleTimeString()
    } else if (new Date() - d < 259200000) {
      // if date is within 3 days specify the full time and date
      return `${d.toLocaleTimeString()} ${d.toLocaleDateString()}`
    }
    // if date is more than 3 days ago only show date
    return d.toLocaleDateString()
  }, [date])
  return timeString
}

export default DateTime
