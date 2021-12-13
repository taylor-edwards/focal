import { FLASK_ENDPOINT } from 'config'
import { createAbortController } from 'utils'

export default function handler(req, res) {
  if (!['POST', 'DELETE'].includes(req.method)) {
    return res.status(405).send('')
  }
  const controller = createAbortController()
  const timer = setTimeout(
    () => controller.abort(),
    FLASK_ENDPOINT.DEFAULT_TIMEOUT,
  )
  return fetch(`${FLASK_ENDPOINT.BASE}/manufacturer/${req.query.manufacturer_id}`, {
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
      `Caught exception or timeout on ${req.method} to /manufacturer`,
      JSON.stringify(req.body),
      err,
    )
    res.status(503).send('')
  }).finally(() => {
    clearTimeout(timer)
  })
}
