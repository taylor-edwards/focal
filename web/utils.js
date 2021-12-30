import { DEFAULT_TIMEOUT } from 'config'

export const noop = () => {}

export const id = () => Math.random().toString(16).substr(2)

const createAbortController = (() => {
  let __AbortController__
  const getAC = () => {
    if (
      typeof window !== 'undefined' &&
      typeof window.AbortController === 'function'
    ) {
      return window.AbortController
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

export const fetchWithTimeout = async (
  endpoint,
  { timeout = DEFAULT_TIMEOUT, asJSON = true, ...params },
) => {
  const controller = createAbortController()
  const timer = setTimeout(() => controller.abort(), timeout)
  const headers = {
    ...(params.headers ?? {}),
  }
  if (asJSON && !headers.hasOwnProperty('Content-Type')) {
    headers['Content-Type'] = 'application/json'
  }
  const response = await fetch(endpoint, {
    ...params,
    headers,
    signal: controller.signal,
  })
  clearTimeout(timer)
  if (!response.ok) {
    throw new Error(`Request failed with HTTP status ${response.status}`)
  }
  if (asJSON) {
    return await response.json()
  }
  return Promise.resolve(response)
}

// use fetchWithAuth for internal authorization in serverside API calls
export const fetchWithAuth = (token, endpoint, params = {}) =>
  fetchWithTimeout(endpoint, {
    ...params,
    headers: {
      ...(params.headers ?? {}),
      Authorization: `Basic ${token}`,
    },
  })

export const parseCookie = cookie => {
  // returns the session token, if any (only usable serverside)
  if (/^token=.+$/.test(cookie)) {
    const token = cookie.slice(cookie.indexOf('=') + 1)
    return decodeURIComponent(token)
  }
  return null
}
