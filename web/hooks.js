import { useEffect } from 'react'

export const useClientside = fn => useEffect(() => {
  if (typeof window !== 'undefined') {
    fn()
  }
}, [fn])
