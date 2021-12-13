export const noop = () => {}

export const id = () => Math.random().toString(16).substr(2)

export const createAbortController = (() => {
  let __AbortController__
  const getAC = () => {
    if (
      typeof window !== 'undefined' &&
      typeof window.AbortController === 'function'
    ) {
      return AbortController
    }
    const { AbortController } = require('node-abort-controller')
    return AbortController
  }
  return (...args) => {
    if (!__AbortController__) {
      __AbortController__ = getAC()
    }
    return new __AbortController__(...args)
  }
})()
