import { FLASK_ENDPOINT } from 'config'
import { createAbortController } from 'utils'
import { fetchAccountDetails } from 'queries'

export default function handler(req, res) {
  if (req.method === 'GET') {
    // if requestor has valid cookie for a session with account_name then:
    return fetchAccountDetails({ accountName: req.query.account_name })
  }
  if (!['POST', 'DELETE'].includes(req.method)) {
    return res.status(405).send('')
  }
  const controller = createAbortController()
  const timer = setTimeout(
    () => controller.abort(),
    FLASK_ENDPOINT.DEFAULT_TIMEOUT,
  )
  return fetch(`${FLASK_ENDPOINT.BASE}/account/${req.query.account_name}`, {
    headers: {
      'Content-Type': 'application/json'
    },
    method: req.method,
    body: JSON.stringify(req.body),
    signal: controller.signal,
  }).then(response => {
    if (response.ok) {
      res.status(response.status).json(response.body)
    } else {
      res.status(response.status).send('')
    }
  }).catch(err => {
    console.log(
      `Caught exception or timeout on ${req.method} to /account`,
      JSON.stringify(req.body),
      err,
    )
    res.status(503).send('')
  }).finally(() => {
    clearTimeout(timer)
  })
}
